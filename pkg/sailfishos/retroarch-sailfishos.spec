Name:           retroarch
Version:        1.16.0
Release:        v1.16.0
Summary:        Official reference frontend for libretro

Group:          Applications/Emulators
License:        GPLv3+
URL:            https://www.libretro.com/

BuildRequires:  wayland-egl-devel
BuildRequires:  pulseaudio-devel
BuildRequires:  OpenAL-devel
BuildRequires:  libudev-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  zlib-devel
BuildRequires:  freetype-devel
#BuildRequires:  ffmpeg-devel
BuildRequires:  SDL2-devel
BuildRequires:  SDL2_image-devel
#Requires libusb 1.0.16
#BuildRequires:  libusb-devel

%description
RetroArch is the official reference frontend for the libretro API.
Libretro is a simple but powerful development interface that allows for the
easy creation of emulators, games and multimedia applications that can plug
straight into any libretro-compatible frontend. This development interface
is open to others so that they can run these pluggable emulator and game
cores also in their own programs or devices.

%build
# No autotools, custom configure script
%ifarch armv7hl aarch64

FLAGS="-DMESA_EGL_NO_X11_HEADERS"
%ifarch aarch64
FLAGS="${FLAGS} -march=armv8.4-a -D__ARM_NEON__ -DHAVE_NEON"
%endif
export CFLAGS="${CFLAGS} ${FLAGS}"
export CXXFLAGS="${CXXFLAGS} ${FLAGS}"

if ! test -f config.h; then
%ifarch armv7hl
./configure --prefix=%{_prefix} --disable-x11 --enable-wayland --enable-opengles --enable-egl --enable-floathard --enable-neon
%else
./configure --prefix=%{_prefix} --disable-x11 --enable-wayland --enable-opengles --enable-opengles3 --enable-opengles3_2 --enable-egl
%endif

%else
./configure --prefix=%{_prefix} --enable-opengles
%endif
fi

make %{?_smp_mflags}


%install
%make_install

# Configuration changes
sed -i \
  's|^# video_fullscreen =.*|video_fullscreen = "true"|;
   s|^# menu_driver =.*|menu_driver = "glui"|;
   s|^# menu_mouse_enable =.*|menu_mouse_enable = "false"|;
   s|^# menu_pointer_enable =.*|menu_pointer_enable = "true"|;
   s|^# input_driver =.*|input_driver = "wayland"|' \
  %{buildroot}/etc/retroarch.cfg

%ifarch armv7hl
sed -i \
  's|^# core_updater_buildbot_url =.*|core_updater_buildbot_cores_url = "https://buildbot.libretro.com/nightly/linux/armv7-neon-hf/latest/"|;' \
  %{buildroot}/etc/retroarch.cfg
%endif

%ifarch aarch64
sed -i \
  's|^# core_updater_buildbot_url =.*|core_updater_buildbot_cores_url = "https://smokku.github.io/RetroArch/Lakka-RPi3.aarch64-4.3/"|;' \
  %{buildroot}/etc/retroarch.cfg
%endif

sed -i \
  's|^Exec=retroarch|Exec=env PULSE_PROP_media.role=x-maemo retroarch --menu --fullscreen|' \
  %{buildroot}/usr/share/applications/retroarch.desktop
  echo '[X-Sailjail]' >> %{buildroot}/usr/share/applications/retroarch.desktop
  echo 'Sandboxing=Disabled' >> %{buildroot}/usr/share/applications/retroarch.desktop

  # Install icon file in the correct place
  mkdir -p %{buildroot}/usr/share/icons/hicolor/86x86/apps
  install -m 644 "./media/retroarch-96x96.png" "%{buildroot}/usr/share/icons/hicolor/86x86/apps/retroarch.png"
  rm "%{buildroot}/usr/share/pixmaps/retroarch.svg"
  rmdir "%{buildroot}/usr/share/pixmaps"

%files
%doc README.md
%config /etc/retroarch.cfg
%{_prefix}/bin/retroarch
%{_prefix}/bin/retroarch-cg2glsl
%{_prefix}/share/applications/retroarch.desktop
%{_prefix}/share/man/man6/*.6*
%{_prefix}/share/icons/hicolor/86x86/apps/retroarch.*
%{_prefix}/share/doc/retroarch/*
%{_prefix}/share/metainfo/*.xml
%changelog
