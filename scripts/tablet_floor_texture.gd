extends RefCounted
## Offline ETC2 trial. Only supported iOS renderers use derived floor storage.
## No Image/Texture references are retained here; drawing-session caches own uploads.
static var enabled := OS.has_feature("ios") and not OS.get_cmdline_user_args().has("--reference-tablet-floor-vram")
static var supported := RenderingServer.has_os_feature("etc2")
static var served := 0
static var cumulative_payload_bytes := 0
const RECORDS = {
  "res://assets/floors-and-details-v3/agriculture-floor.png": {
    "resource": "res://assets/tablet-floor-vram/agriculture-floor.res",
    "sha256": "25baab3652d76f97adc245e9ad7ebf2f1762bdfe4072e363d37c14ed12f6f8ee",
    "width": 1254,
    "height": 1254,
    "format": 30
  },
  "res://assets/room-floor-tiles-v4/server-rubber.png": {
    "resource": "res://assets/tablet-floor-vram/server-rubber.res",
    "sha256": "43420a3ec05c1b08df646adfbac8b2486373af61adc9e2c2db8fa73001bbf2b6",
    "width": 1254,
    "height": 1254,
    "format": 30
  },
  "res://assets/department-floors-v2/brine-ceramic.png": {
    "resource": "res://assets/tablet-floor-vram/brine-ceramic.res",
    "sha256": "68e3d511374255d724cde2bda5e08d3bc2ff5f8708fc9c4d5b88305efd031c67",
    "width": 1254,
    "height": 1254,
    "format": 30
  },
  "res://assets/department-floors-v1/habitation-composite.png": {
    "resource": "res://assets/tablet-floor-vram/habitation-composite.res",
    "sha256": "6d61be8c35cd3a10cd7d7021d10fcd2e0df97a9eb3e71c1ad67c6e4309d69b58",
    "width": 1254,
    "height": 1254,
    "format": 30
  },
  "res://assets/department-floors-v2/storage-load-deck.png": {
    "resource": "res://assets/tablet-floor-vram/storage-load-deck.res",
    "sha256": "95aaf0bb8c3987d4855d6c56510e83e887f57b84f3bcd5d77340c029a18f4fa0",
    "width": 1254,
    "height": 1254,
    "format": 30
  },
  "res://assets/department-floors-v1/medical-sealed.png": {
    "resource": "res://assets/tablet-floor-vram/medical-sealed.res",
    "sha256": "541e947c24d44519840b2f6dfab8112fb55d34673b72247d068198c08e30cf2d",
    "width": 1254,
    "height": 1254,
    "format": 30
  },
  "res://assets/department-floors-v2/robotics-service.png": {
    "resource": "res://assets/tablet-floor-vram/robotics-service.res",
    "sha256": "1b28908a73cecc263b2e4f70b122d5a3b0ce57ea1822700dccc12fb2741220f7",
    "width": 1254,
    "height": 1254,
    "format": 30
  },
  "res://assets/department-floors-v1/engineering-tread.png": {
    "resource": "res://assets/tablet-floor-vram/engineering-tread.res",
    "sha256": "e0654dbb646f557a8abd985dd324f286f7ec64cdd62b23b505fc4394336008b0",
    "width": 1254,
    "height": 1254,
    "format": 30
  },
  "res://assets/department-floors-v1/wet-drainage.png": {
    "resource": "res://assets/tablet-floor-vram/wet-drainage.res",
    "sha256": "756129f8685ebfc26b891c60f45bc6d5bda7c1b87921f1a588089ba494038fb4",
    "width": 1254,
    "height": 1254,
    "format": 30
  }
}

static func image_for(source: String) -> Image:
	if not enabled or not supported or not RECORDS.has(source): return null
	var record: Dictionary = RECORDS[source]
	var path: String = record.resource
	if not ResourceLoader.exists(path): return null
	var image = ResourceLoader.load(path, "Image", ResourceLoader.CACHE_MODE_IGNORE)
	if not valid_image(image, source, record): return null
	served += 1
	cumulative_payload_bytes += image.get_data_size()
	return image

static func valid_image(image: Resource, source: String, record: Dictionary) -> bool:
	return image is Image and image.is_compressed() and not image.has_mipmaps() \
		and image.get_width() == record.width and image.get_height() == record.height \
		and image.get_format() == record.format \
		and image.get_meta("source_path", "") == source \
		and image.get_meta("source_sha256", "") == record.sha256
