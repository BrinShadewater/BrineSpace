// Validation wrapper only. Never linked into frozen/public builds automatically.
#include <mach/mach.h>
#include <pthread.h>
#include <sys/qos.h>
#include <time.h>
#include <unistd.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

namespace {
struct VmCategory {
    uint64_t regions = 0, virtual_bytes = 0, resident_bytes = 0, dirty_bytes = 0;
};
uint64_t monotonic_usec() {
    struct timespec value = {};
    clock_gettime(CLOCK_MONOTONIC, &value);
    return static_cast<uint64_t>(value.tv_sec) * 1000000 + value.tv_nsec / 1000;
}
const char *vm_category_name(unsigned tag) {
    switch (tag) {
        case VM_MEMORY_MALLOC: return "malloc";
        case VM_MEMORY_MALLOC_SMALL: return "malloc_small";
        case VM_MEMORY_MALLOC_LARGE: return "malloc_large";
        case VM_MEMORY_MALLOC_HUGE: return "malloc_huge";
        case VM_MEMORY_MALLOC_TINY: return "malloc_tiny";
        case VM_MEMORY_MALLOC_NANO: return "malloc_nano";
        case VM_MEMORY_MALLOC_MEDIUM: return "malloc_medium";
        case VM_MEMORY_IOKIT: return "iokit";
        case VM_MEMORY_IOSURFACE: return "iosurface";
        case VM_MEMORY_STACK: return "stack";
        case VM_MEMORY_COREGRAPHICS: return "coregraphics";
        case VM_MEMORY_IMAGEIO: return "imageio";
        default: return "other";
    }
}
// Opt-in, aggregate-only diagnostic. No addresses, mapped filenames, stack
// contents or memory contents are read or written. Resident VM pages can alias;
// their sum is not the process's charged physical footprint or a GPU inventory.
void requested_vm_snapshot(const char *home) {
    char request[PATH_MAX], destination[PATH_MAX], temporary[PATH_MAX];
    int n = snprintf(request, sizeof(request), "%s/Documents/qa_vm_snapshot.request", home);
    if (n < 0 || static_cast<size_t>(n) >= sizeof(request) || unlink(request) != 0) return;
    n = snprintf(destination, sizeof(destination), "%s/Documents/qa_vm_snapshot.json", home);
    if (n < 0 || static_cast<size_t>(n) >= sizeof(destination)) return;
    n = snprintf(temporary, sizeof(temporary), "%s/Documents/qa_vm_snapshot.tmp", home);
    if (n < 0 || static_cast<size_t>(n) >= sizeof(temporary)) return;
    const uint64_t start = monotonic_usec();
    VmCategory categories[257] = {};
    vm_address_t address = 0;
    natural_t depth = 0;
    unsigned regions = 0;
    bool complete = false;
    kern_return_t error = KERN_SUCCESS;
    const uint64_t page_size = static_cast<uint64_t>(getpagesize());
    while (regions < 65536 && monotonic_usec() - start < 500000) {
        vm_size_t size = 0;
        vm_region_submap_info_data_64_t info = {};
        mach_msg_type_number_t count = VM_REGION_SUBMAP_INFO_COUNT_64;
        error = vm_region_recurse_64(mach_task_self(), &address, &size, &depth,
                reinterpret_cast<vm_region_recurse_info_t>(&info), &count);
        if (error != KERN_SUCCESS) {
            complete = error == KERN_INVALID_ADDRESS;
            break;
        }
        if (info.is_submap) {
            if (++depth > 64) break;
            continue;
        }
        const unsigned tag = info.user_tag < 256 ? info.user_tag : 256;
        VmCategory &category = categories[tag];
        ++category.regions;
        ++regions;
        category.virtual_bytes += size;
        category.resident_bytes += static_cast<uint64_t>(info.pages_resident) * page_size;
        category.dirty_bytes += static_cast<uint64_t>(info.pages_dirtied) * page_size;
        if (!size || address > UINTPTR_MAX - size) break;
        address += size;
    }
    task_vm_info_data_t task = {};
    mach_msg_type_number_t count = TASK_VM_INFO_COUNT;
    const kern_return_t task_error = task_info(mach_task_self(), TASK_VM_INFO,
            reinterpret_cast<task_info_t>(&task), &count);
    FILE *file = fopen(temporary, "w");
    if (!file) return;
    bool ok = fprintf(file,
            "{\"pid\":%d,\"epoch\":%lld,\"complete\":%s,\"error\":%d,\"regions\":%u,"
            "\"elapsed_usec\":%llu,\"footprint_valid\":%s,\"footprint_bytes\":%llu,"
            "\"scope\":\"Aggregate VM region pages; may alias; not additive to physical footprint\",\"categories\":[",
            getpid(), static_cast<long long>(time(nullptr)), complete ? "true" : "false", error,
            regions, static_cast<unsigned long long>(monotonic_usec() - start),
            task_error == KERN_SUCCESS && count >= TASK_VM_INFO_REV1_COUNT ? "true" : "false",
            static_cast<unsigned long long>(task_error == KERN_SUCCESS && count >= TASK_VM_INFO_REV1_COUNT ? task.phys_footprint : 0)) >= 0;
    bool first = true;
    for (unsigned tag = 0; tag < 257; ++tag) {
        const VmCategory &category = categories[tag];
        if (!category.regions) continue;
        ok = fprintf(file,
                "%s{\"tag\":%u,\"name\":\"%s\",\"regions\":%llu,\"virtual_bytes\":%llu,\"resident_bytes\":%llu,\"dirty_bytes\":%llu}",
                first ? "" : ",", tag, vm_category_name(tag),
                static_cast<unsigned long long>(category.regions),
                static_cast<unsigned long long>(category.virtual_bytes),
                static_cast<unsigned long long>(category.resident_bytes),
                static_cast<unsigned long long>(category.dirty_bytes)) >= 0 && ok;
        first = false;
    }
    ok = fprintf(file, "]}\n") >= 0 && ok;
    ok = fclose(file) == 0 && ok;
    if (ok) rename(temporary, destination);
    else unlink(temporary);
}
void *sample_memory(void *) {
    pthread_set_qos_class_self_np(QOS_CLASS_UTILITY, 0);
    const char *home = getenv("HOME");
    char path[PATH_MAX];
    if (!home) return nullptr;
    const int length = snprintf(path, sizeof(path), "%s/Documents/qa_native_memory.jsonl", home);
    if (length < 0 || static_cast<size_t>(length) >= sizeof(path)) return nullptr;
    FILE *file = fopen(path, "w");
    if (!file) return nullptr;
    unsigned rows = 0;
    uint64_t observed_max = 0;
    for (;;) {
        task_vm_info_data_t info = {};
        mach_msg_type_number_t count = TASK_VM_INFO_COUNT;
        const kern_return_t error = task_info(mach_task_self(), TASK_VM_INFO,
                reinterpret_cast<task_info_t>(&info), &count);
        struct timespec clock = {};
        clock_gettime(CLOCK_MONOTONIC, &clock);
        const double uptime = clock.tv_sec + clock.tv_nsec / 1e9;
        const bool valid = error == KERN_SUCCESS && count >= TASK_VM_INFO_REV1_COUNT;
        const uint64_t footprint = valid ? info.phys_footprint : 0;
        if (footprint > observed_max) observed_max = footprint;
        if (rows == 1800) {
            file = freopen(path, "w", file);
            if (!file) return nullptr;
            rows = 0;
        }
        if (fprintf(file, "{\"pid\":%d,\"epoch\":%lld,\"uptime_seconds\":%.6f,\"valid\":%s,\"error\":%d,\"footprint_bytes\":%llu,\"resident_bytes\":%llu,\"sampled_max_bytes\":%llu}\n",
                getpid(), static_cast<long long>(time(nullptr)), uptime,
                valid ? "true" : "false", error,
                static_cast<unsigned long long>(footprint),
                static_cast<unsigned long long>(valid ? info.resident_size : 0),
                static_cast<unsigned long long>(observed_max)) < 0 || fflush(file) != 0) {
            fclose(file);
            return nullptr;
        }
        ++rows;
        requested_vm_snapshot(home);
        sleep(1);
    }
}
pthread_once_t sampler_once = PTHREAD_ONCE_INIT;
void start_sampler_once() {
    pthread_t thread;
    if (pthread_create(&thread, nullptr, sample_memory, nullptr) == 0) pthread_detach(thread);
}
}
void brinespace_qa_memory_start() { pthread_once(&sampler_once, start_sampler_once); }
#ifdef BRINESPACE_QA_MEMORY_TEST
int main() { brinespace_qa_memory_start(); sleep(3); return 0; }
#endif
