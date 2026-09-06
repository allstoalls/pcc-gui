
#import <AppKit/AppKit.h>
#include <stdint.h>
#include <stdio.h>
void *pcc_gui_metal_window_create(const char *, int64_t, int64_t);
int64_t pcc_gui_metal_window_close(void *);
int64_t pcc_gui_metal_lifecycle_install(void *, uint64_t, void *);
int64_t pcc_gui_metal_lifecycle_probe(void *, const char *);
static int callbacks = 0;
static int32_t receive(int32_t kind, uint64_t window, const void *payload,
                       uint64_t length, int32_t flags, int32_t code) {
  callbacks++;
  return 0;
}
int main(void) {
  for (int i = 0; i < 3; i++) {
    __weak NSWindow *observed;
    @autoreleasepool {
      void *handle = pcc_gui_metal_window_create("window ownership", 320, 200);
      if (!handle) return 1;
      observed = (__bridge NSWindow *)handle;
      if (pcc_gui_metal_lifecycle_install(handle, 77, (void *)receive)) return 2;
      if (pcc_gui_metal_lifecycle_probe(handle, "/tmp/opened.txt")) return 3;
      if (pcc_gui_metal_window_close(handle)) return 4;
    }
    if (observed != nil) return 5;
  }
  if (callbacks < 9) return 6;
  puts("PCC_WINDOW_CLOSE_OWNERSHIP_OK cycles=3 retained_windows=0");
  return 0;
}
