"""The validation sampler must report real resident VM categories on demand."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


@unittest.skipUnless(sys.platform == "darwin", "Darwin validation sampler")
class MemorySnapshotTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scratch = tempfile.TemporaryDirectory(prefix="brinespace-vm-test-")
        cls.root = Path(cls.scratch.name)
        sampler = Path(__file__).resolve().parents[1] / "tools/qa_native_memory_sampler.cpp"
        driver = cls.root / "driver.cpp"
        driver.write_text('''
#include <stdlib.h>
#include <unistd.h>
void brinespace_qa_memory_start();
int main(int argc, char **argv) {
    size_t bytes = strtoull(argv[1], nullptr, 10);
    volatile char *data = static_cast<volatile char *>(malloc(bytes));
    for (size_t i = 0; i < bytes; i += 4096) data[i] = 1;
    brinespace_qa_memory_start();
    sleep(3);
    free(const_cast<char *>(data));
}
''')
        cls.binary = cls.root / "sampler-test"
        subprocess.run(["xcrun", "clang++", "-std=c++17", str(sampler),
                        str(driver), "-o", str(cls.binary)], check=True, capture_output=True)

    @classmethod
    def tearDownClass(cls):
        cls.scratch.cleanup()

    def capture(self, label, allocated_bytes, request=True):
        home = self.root / label
        documents = home / "Documents"
        documents.mkdir(parents=True)
        marker = documents / "qa_vm_snapshot.request"
        if request:
            marker.write_text("1")
        subprocess.run([str(self.binary), str(allocated_bytes)],
                       env=dict(os.environ, HOME=str(home)), check=True, timeout=10)
        snapshot = documents / "qa_vm_snapshot.json"
        self.assertEqual(snapshot.exists(), request, "Snapshot must be explicitly requested")
        self.assertFalse(marker.exists(), "Requested snapshot must be acknowledged")
        if request:
            value = json.loads(snapshot.read_text())
            self.assertTrue(value["complete"])
            self.assertGreater(value["regions"], 0)
            self.assertGreater(value["footprint_bytes"], 0)
            self.assertGreater(value["elapsed_usec"], 0)
            self.assertLessEqual(len(value["categories"]), 257)
            return value

    def test_requested_categories_detect_touched_heap_allocation(self):
        before = self.capture("baseline", 0)
        after = self.capture("allocated", 64 * 1024 * 1024)
        # Darwin VM_MEMORY_MALLOC_LARGE is tag 3; expectations come from the SDK,
        # not from the sampler's category mapping or total process footprint.
        def large_resident(snapshot):
            return sum(row["resident_bytes"] for row in snapshot["categories"] if row["tag"] == 3)
        self.assertGreaterEqual(large_resident(after) - large_resident(before), 60 * 1024 * 1024)

    def test_no_category_walk_without_explicit_request(self):
        self.capture("no-request", 0, request=False)


if __name__ == "__main__":
    unittest.main()
