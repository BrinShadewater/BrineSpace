Add-Type -AssemblyName System.Drawing
$artRoot = $PSScriptRoot
$original = [System.Drawing.Bitmap]::new((Join-Path $artRoot '../consistency-v1/cover.png'))
$generated = [System.Drawing.Image]::FromFile((Join-Path $artRoot 'head-candidate-02.png'))
$patch = [System.Drawing.Bitmap]::new(180,200)
$graphics = [System.Drawing.Graphics]::FromImage($patch)
$graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$graphics.DrawImage($generated,0,0,180,200)
$graphics.Dispose()
$result = $original.Clone()
$changed = 0
for ($y=0;$y -lt 200;$y++) {
 for ($x=0;$x -lt 180;$x++) {
  # Feather within facial skin; leave hair, silhouette, body and stage unchanged.
  $radius = [Math]::Sqrt([Math]::Pow(($x*4-350)/174.0,2)+[Math]::Pow(($y*4-405)/225.0,2))
  if ($radius -ge 1) { continue }
  $alpha = [Math]::Min(1,(1-$radius)/0.12)
  $alpha = $alpha*$alpha*(3-2*$alpha)
  $before = $original.GetPixel(875+$x,180+$y)
  $after = $patch.GetPixel($x,$y)
  $color = [System.Drawing.Color]::FromArgb(255,[int][Math]::Round($before.R*(1-$alpha)+$after.R*$alpha),[int][Math]::Round($before.G*(1-$alpha)+$after.G*$alpha),[int][Math]::Round($before.B*(1-$alpha)+$after.B*$alpha))
  $result.SetPixel(875+$x,180+$y,$color)
  if ($color.ToArgb() -ne $before.ToArgb()) { $changed++ }
 }
}
$result.Save((Join-Path $artRoot 'cover.png'),[System.Drawing.Imaging.ImageFormat]::Png)
$outsideChanges = 0
for ($y=0;$y -lt $original.Height;$y++) {
 for ($x=0;$x -lt $original.Width;$x++) {
  if ($x -ge 875 -and $x -lt 1055 -and $y -ge 180 -and $y -lt 380) {continue}
  if ($original.GetPixel($x,$y).ToArgb() -ne $result.GetPixel($x,$y).ToArgb()) {$outsideChanges++}
 }
}
Write-Output "Changed facial pixels: $changed; outside-region differences: $outsideChanges; size: $($result.Width)x$($result.Height)"
if ($outsideChanges -ne 0) {throw 'Unexpected changes outside face region'}
$board=[System.Drawing.Bitmap]::new(1080,600)
$boardGraphics=[System.Drawing.Graphics]::FromImage($board)
$boardGraphics.InterpolationMode=[System.Drawing.Drawing2D.InterpolationMode]::NearestNeighbor
foreach($entry in @(@{Image=$original; X=0},@{Image=$result; X=540})) {
 $boardGraphics.DrawImage($entry.Image,[System.Drawing.Rectangle]::new($entry.X,0,540,600),875,180,180,200,[System.Drawing.GraphicsUnit]::Pixel)
}
$board.Save((Join-Path $artRoot 'before-after.png'),[System.Drawing.Imaging.ImageFormat]::Png)
$boardGraphics.Dispose();$board.Dispose();$result.Dispose();$patch.Dispose();$generated.Dispose();$original.Dispose()
