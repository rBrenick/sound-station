# sound-station
Basic website for queueing up and playing youtube videos on a remote computer.

# Why?
I wanted to set up an office computer to some speakers (for music). But I didn't wanna have to get up and press buttons on it all the time.

I imagine most people would just RemoteDesktop and control it manually.

Or find an existing app/software that does this.

Or use a playlist.

But where's the fun in any of that, when I can instead spend hours to make 1% of the features in a janky homebrew.

# How?
Written mostly to experiment with Selenium, and using HTML/JS as frontends for Python functionality. I wouldn't expect to be able to use this out of the box. Just making it public to share.

Running _'start_standalone.bat'_ will boot up a SimpleHTTPRequestHandler python server.

In the _/website/_ folder you'll find some handwritten HTML and Javascript that triggers GET requests on that server.

![tool header image](docs/header_image.PNG)
