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
