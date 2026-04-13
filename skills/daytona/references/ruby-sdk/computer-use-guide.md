## Contents

- Start Computer Use
- Stop Computer Use
- Get status
- Get process status
- Restart process
- Get process logs
- Get process errors
- Mouse operations
- Keyboard operations
- Screenshot operations
- Screen Recording
- Display operations
- See Also




Computer Use enables programmatic control of desktop environments within sandboxes. It provides mouse, keyboard, screenshot, screen recording, and display operations for automating GUI interactions and testing desktop applications.

Computer Use and [VNC](./vnc-access.md) work together to enable both manual and automated desktop interactions. VNC provides the visual interface for users to manually interact with the desktop, while Computer Use provides the programmatic API for AI agents to automate operations.

Computer Use is available for **Linux**. **Windows** and **macOS** support is currently in private alpha.
> **Caution: Private Alpha**
> Computer Use for macOS and Windows is currently in private alpha and requires access. To request access, fill out the [Windows](https://docs.google.com/forms/d/e/1FAIpQLSfoK-77-VpfsMubw8F4f1opCxIL1AyJUgnM0ONYup5hZ0RTvQ/viewform?usp=dialog) or [macOS](https://docs.google.com/forms/d/e/1FAIpQLSc9xlGZ49OjWNkyzDPC9Ip3InMRR0ZXY3tcoD-PFQj3ck6gzQ/viewform?usp=sharing&ouid=103304973264148733944) access request form. Our team will review your request and reach out with setup instructions.

- **GUI application testing**: automate interactions with native applications, click buttons, fill forms, and validate UI behavior
- **Visual testing & screenshots**: capture screenshots of applications, compare UI states, and perform visual regression testing
- **Desktop automation**: automate repetitive desktop tasks, file management through GUI, and complex workflows

## Start Computer Use

Start all computer use processes (Xvfb, xfce4, x11vnc, novnc) in the Sandbox.

```ruby
result = sandbox.computer_use.start
puts "Computer use processes started: #{result.message}"
```

## Stop Computer Use

Stop all computer use processes in the Sandbox.

```ruby
result = sandbox.computer_use.stop
puts "Computer use processes stopped: #{result.message}"
```

## Get status

Get the status of all computer use processes.

```ruby
response = sandbox.computer_use.status
puts "Computer use status: #{response.status}"
```

## Get process status

Get the status of a specific VNC process.

```ruby
xvfb_status = sandbox.computer_use.get_process_status("xvfb")
no_vnc_status = sandbox.computer_use.get_process_status("novnc")
```

## Restart process

Restart a specific VNC process.

```ruby
result = sandbox.computer_use.restart_process("xfce4")
puts "XFCE4 process restarted: #{result.message}"
```

## Get process logs

Get logs for a specific VNC process.

```ruby
logs = sandbox.computer_use.get_process_logs("novnc")
puts "NoVNC logs: #{logs}"
```

## Get process errors

Get error logs for a specific VNC process.

```ruby
errors = sandbox.computer_use.get_process_errors("x11vnc")
puts "X11VNC errors: #{errors}"
```

## Mouse operations

### Click

Click the mouse at the specified coordinates.

```ruby
# Single left click
result = sandbox.computer_use.mouse.click(x: 100, y: 200)

# Double click
double_click = sandbox.computer_use.mouse.click(x: 100, y: 200, button: 'left', double: true)

# Right click
right_click = sandbox.computer_use.mouse.click(x: 100, y: 200, button: 'right')
```

### Move

Move the mouse cursor to the specified coordinates.

```ruby
result = sandbox.computer_use.mouse.move(x: 100, y: 200)
puts "Mouse moved to: #{result.x}, #{result.y}"
```

### Drag

Drag the mouse from start coordinates to end coordinates.

```ruby
result = sandbox.computer_use.mouse.drag(start_x: 50, start_y: 50, end_x: 150, end_y: 150)
puts "Dragged from #{result.from_x},#{result.from_y} to #{result.to_x},#{result.to_y}"
```

### Scroll

Scroll the mouse wheel at the specified coordinates.

```ruby
# Scroll up
scroll_up = sandbox.computer_use.mouse.scroll(x: 100, y: 200, direction: 'up', amount: 3)

# Scroll down
scroll_down = sandbox.computer_use.mouse.scroll(x: 100, y: 200, direction: 'down', amount: 5)
```

### Get position

Get the current mouse cursor position.

```ruby
position = sandbox.computer_use.mouse.position
puts "Mouse is at: #{position.x}, #{position.y}"
```

## Keyboard operations

### Type

Type the specified text.

```ruby
sandbox.computer_use.keyboard.type(text: "Hello, World!")

# With delay between characters
sandbox.computer_use.keyboard.type(text: "Slow typing", delay: 100)
```

### Press

Press a key with optional modifiers.

```ruby
# Press Enter
sandbox.computer_use.keyboard.press(key: "Return")

# Press Ctrl+C
sandbox.computer_use.keyboard.press(key: "c", modifiers: ["ctrl"])

# Press Ctrl+Shift+T
sandbox.computer_use.keyboard.press(key: "t", modifiers: ["ctrl", "shift"])
```

### Hotkey

Press a hotkey combination.

```ruby
# Copy
sandbox.computer_use.keyboard.hotkey(keys: "ctrl+c")

# Paste
sandbox.computer_use.keyboard.hotkey(keys: "ctrl+v")

# Alt+Tab
sandbox.computer_use.keyboard.hotkey(keys: "alt+tab")
```

## Screenshot operations

### Take full screen

Take a screenshot of the entire screen.

```ruby
screenshot = sandbox.computer_use.screenshot.take_full_screen
puts "Screenshot size: #{screenshot.width}x#{screenshot.height}"

# With cursor visible
with_cursor = sandbox.computer_use.screenshot.take_full_screen(show_cursor: true)
```

### Take region

Take a screenshot of a specific region.

```ruby
region = Daytona::ComputerUse::ScreenshotRegion.new(x: 100, y: 100, width: 300, height: 200)
screenshot = sandbox.computer_use.screenshot.take_region(region: region)
puts "Captured region: #{screenshot.region.width}x#{screenshot.region.height}"
```

### Take compressed

Take a compressed screenshot of the entire screen.

```ruby
# Default compression
screenshot = sandbox.computer_use.screenshot.take_compressed

# High quality JPEG
jpeg = sandbox.computer_use.screenshot.take_compressed(
  options: Daytona::ComputerUse::ScreenshotOptions.new(format: "jpeg", quality: 95, show_cursor: true)
)

# Scaled down PNG
scaled = sandbox.computer_use.screenshot.take_compressed(
  options: Daytona::ComputerUse::ScreenshotOptions.new(format: "png", scale: 0.5)
)
```

### Take compressed region

Take a compressed screenshot of a specific region.

```ruby
region = Daytona::ComputerUse::ScreenshotRegion.new(x: 0, y: 0, width: 800, height: 600)
screenshot = sandbox.computer_use.screenshot.take_compressed_region(
  region: region,
  options: Daytona::ComputerUse::ScreenshotOptions.new(format: "webp", quality: 80, show_cursor: true)
)
puts "Compressed size: #{screenshot.size_bytes} bytes"
```

## Screen Recording

Computer Use supports screen recording capabilities, allowing you to capture desktop sessions for debugging, documentation, or automation workflows.

### Configure Recording Directory

By default, recordings are saved to `~/.daytona/recordings`. You can specify a custom directory by passing the `DAYTONA_RECORDINGS_DIR` environment variable when creating a sandbox:

```ruby
require 'daytona'

daytona = Daytona::Client.new
sandbox = daytona.create(
  snapshot: 'daytonaio/sandbox:0.6.0',
  name: 'my-sandbox',
  env_vars: { DAYTONA_RECORDINGS_DIR: '/home/daytona/my-recordings' }
)
```

### Start Recording

Start a new screen recording session with an optional name identifier:

```ruby
# Start recording with a custom label
recording = sandbox.computer_use.recording.start(label: 'test-1')
puts "Recording started: #{recording.id}"
puts "File path: #{recording.file_path}"
```

### Stop Recording

Stop an active recording session by providing the recording ID:

```ruby
# Stop the recording
stopped_recording = sandbox.computer_use.recording.stop(id: recording.id)
puts "Recording stopped: #{stopped_recording.duration_seconds} seconds"
puts "Saved to: #{stopped_recording.file_path}"
```

### List Recordings

Get a list of all recordings in the sandbox:

```ruby
recordings_list = sandbox.computer_use.recording.list
puts "Total recordings: #{recordings_list.recordings.length}"
recordings_list.recordings.each do |rec|
  puts "- #{rec.name}: #{rec.duration_seconds}s (#{rec.file_size_bytes} bytes)"
end
```

### Get Recording

Get details about a specific recording:

```ruby
recording_detail = sandbox.computer_use.recording.get(id: 'recording-id')
puts "Recording: #{recording_detail.name}"
puts "Status: #{recording_detail.status}"
puts "Duration: #{recording_detail.duration_seconds}s"
```

### Delete Recording

Delete a recording by ID:

```ruby
sandbox.computer_use.recording.delete(id: 'recording-id')
puts 'Recording deleted successfully'
```

### Download Recording

Download a recording file from the sandbox to your local machine. The file is streamed efficiently without loading the entire content into memory, making it suitable for large recordings.

```ruby
# Download recording to local file
sandbox.computer_use.recording.download(id: recording.id, local_path: 'local_recording.mp4')
puts 'Recording downloaded successfully'

# Or with custom path
download_path = "recordings/recording_#{recording.id}.mp4"
sandbox.computer_use.recording.download(id: recording.id, local_path: download_path)
```
> **Tip: Streaming Downloads**
> All SDK implementations stream the recording file directly to disk without loading the entire content into memory. This allows you to download large recordings (hundreds of MB or even GB) efficiently without running out of memory.
>
> - **Python**: Streams in 64KB chunks using `httpx`
> - **TypeScript**: Uses Node.js `pipeline()` with backpressure handling
> - **Ruby**: Uses Typhoeus streaming with `on_body` callbacks
> - **Go**: Uses `io.Copy()` with 32KB internal buffer

### Recording Dashboard

Every sandbox includes a built-in recording dashboard for managing screen recordings through a web interface. The dashboard allows you to view, download, and delete recordings without writing code.

To access the recording dashboard:

1. Navigate to your sandboxes in the Daytona Dashboard
2. Click the action menu (three dots) for your sandbox
3. Select **Screen Recordings** from the dropdown menu

The recording dashboard provides:
- List of all recordings with metadata (name, duration, file size, creation time)
- Playback controls for reviewing recordings
- Download functionality to save recordings locally
- Delete options for managing storage
> **Tip:**
> The recording dashboard runs on a private port and is automatically secured. No additional authentication is required once you access it through the Daytona Dashboard.

## Display operations

### Get info

Get information about the displays.

```ruby
info = sandbox.computer_use.display.info
puts "Primary display: #{info.primary_display.width}x#{info.primary_display.height}"
puts "Total displays: #{info.total_displays}"
info.displays.each_with_index do |display, i|
  puts "Display #{i}: #{display.width}x#{display.height} at #{display.x},#{display.y}"
end
```

### Get windows

Get the list of open windows.

```ruby
windows = sandbox.computer_use.display.windows
puts "Found #{windows.count} open windows:"
windows.windows.each do |window|
  puts "- #{window.title} (ID: #{window.id})"
end
```

## See Also
- [Ruby SDK - computer-use](./computer-use.md)
- [Python SDK - computer-use-guide](../python-sdk/computer-use-guide.md)
- [TypeScript SDK - computer-use-guide](../typescript-sdk/computer-use-guide.md)
- [Go SDK - computer-use-guide](../go-sdk/computer-use-guide.md)
