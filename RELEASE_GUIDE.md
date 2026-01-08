# GitHub Release Guide for Space N Aliens

## Step 1: Build the Executable (Already Done!)
The executable should now be in the `dist/` folder as `SpaceNAliens.exe`

## Step 2: Test the Executable
1. Navigate to `dist/` folder
2. Double-click `SpaceNAliens.exe` to test it
3. Make sure the game runs properly

## Step 3: Create a GitHub Release

### Option A: Using GitHub Website (Recommended for first-time)
1. Go to your repository: https://github.com/tbaaaa/space-n-aliens
2. Click on "Releases" (right side of the page)
3. Click "Draft a new release" or "Create a new release"
4. Fill in:
   - **Tag version**: v1.5 (or your version number)
   - **Release title**: Space N Aliens v1.5 - Visual Overhaul
   - **Description**: 
     ```
     ## What's New
     - Player ship now rotates toward mouse cursor
     - Unique designs for all enemy types
     - Custom turret graphics
     - Yellowish environment after Boss 1
     - Smoother hyperdrive effects
     
     ## Download
     Download `SpaceNAliens.exe` and run - no installation required!
     ```
5. Drag and drop `SpaceNAliens.exe` from the `dist/` folder into the "Attach binaries" area
6. Check "Set as the latest release"
7. Click "Publish release"

### Option B: Using Git Command Line
```bash
# Create and push a tag
git tag -a v1.5 -m "Visual Overhaul Release"
git push origin v1.5

# Then go to GitHub website and upload the executable to the release
```

## Step 4: Update README Link
The releases page link in your README should now work:
https://github.com/tbaaaa/space-n-aliens/releases

## Tips:
- Keep the .exe file size in mind (should be around 10-30 MB)
- You can also zip the executable if you want to reduce download size
- Consider adding a virus scan report link (VirusTotal) to build trust
- Update the version number in your game code for future releases
