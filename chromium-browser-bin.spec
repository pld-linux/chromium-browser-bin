%define		svnver  32507
%define		rel		0.1
Summary:	A WebKit powered web browser
Name:		chromium-browser-bin
Version:	4.0.253.0
Release:	0.%{svnver}.%{rel}
License:	BSD, LGPL v2+ (ffmpeg)
Group:		X11/Applications/Networking
Source0:	http://build.chromium.org/buildbot/snapshots/chromium-rel-linux-64/%{svnver}/chrome-linux.zip
# NoSource0-md5:	bc8f6ac27ca2eb92ecb34703b205217c
NoSource:	0
Source2:	chromium-browser.sh
Source3:	chromium-browser.desktop
Source4:	find-lang.sh
BuildRequires:	rpmbuild(macros) >= 1.453
Requires:	browser-plugins >= 2.0
Requires:	nspr
Requires:	nss
Requires:	xdg-utils
Provides:	wwwbrowser
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		find_lang 	sh find-lang.sh %{buildroot}

%define		_enable_debug_packages	0
%define		no_install_post_strip	1

%define		nss_caps	libfreebl3.so libnss3.so libnssckbi.so libsmime3.so ibsoftokn3.so libssl3.so libnssutil3.so
%define		nspr_caps	libnspr4.so libplc4.so libplds4.so
%define		ffmpeg_caps	libavcodec.so libavformat.so libavutil.so

# list of script capabilities (regexps) not to be used in Provides
%define		_noautoprov		%{nss_caps} %{nspr_caps} %{ffmpeg_caps}
%define		_noautoreq		%{_noautoprov}

%description
Chromium is an open-source web browser, powered by WebKit.

%prep
%setup -qc
%{__sed} -e 's,@localedir@,%{_libdir}/%{name},' %{SOURCE4} > find-lang.sh

mv chrome-linux/product_logo_48.png .
mv chrome-linux/chromium-browser.1 .
mv chrome-linux/chrome-wrapper .
mv chrome-linux/{chrome,chromium-browser}
chmod a+x chrome-linux/lib*.so*

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name}/plugins,%{_mandir}/man1,%{_pixmapsdir},%{_desktopdir}}

install -p %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/chromium-browser
%{__sed} -i -e 's,@libdir@,%{_libdir}/%{name},' $RPM_BUILD_ROOT%{_bindir}/chromium-browser
cp -a chrome-linux/* $RPM_BUILD_ROOT%{_libdir}/%{name}
cp -a chromium-browser.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -a product_logo_48.png $RPM_BUILD_ROOT%{_pixmapsdir}/chromium-browser.png
cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}

%browser_plugins_add_browser %{name} -p %{_libdir}/%{name}/plugins

# nspr symlinks
for a in libnspr4.so libplc4.so libplds4.so; do
	ln -s %{_libdir}/$a $RPM_BUILD_ROOT%{_libdir}/%{name}/$a.0d
done
# nss symlinks
for a in libnss3.so libnssutil3.so libsmime3.so libssl3.so; do
	ln -s %{_libdir}/$a $RPM_BUILD_ROOT%{_libdir}/%{name}/$a.1d
done

# find locales
%find_lang %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_browser_plugins

%postun
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files -f %{name}.lang
%defattr(644,root,root,755)

%{_browserpluginsconfdir}/browsers.d/%{name}.*
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{name}.*.blacklist

%attr(755,root,root) %{_bindir}/chromium-browser
%{_mandir}/man1/chromium-browser.1*
%{_pixmapsdir}/chromium-browser.png
%{_desktopdir}/*.desktop
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/chrome.pak
%dir %{_libdir}/%{name}/locales
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/resources
#%{_libdir}/%{name}/themes
%attr(755,root,root) %{_libdir}/%{name}/chromium-browser

# These unique permissions are intentional and necessary for the sandboxing
%attr(4555,root,root) %{_libdir}/%{name}/chrome_sandbox

# ffmpeg libs
%attr(755,root,root) %{_libdir}/%{name}/libffmpegsumo.so
#%attr(755,root,root) %{_libdir}/%{name}/libavcodec.so.52
#%attr(755,root,root) %{_libdir}/%{name}/libavformat.so.52
#%attr(755,root,root) %{_libdir}/%{name}/libavutil.so.50

# nspr/nss symlinks
%attr(755,root,root) %{_libdir}/%{name}/libnspr4.so.0d
%attr(755,root,root) %{_libdir}/%{name}/libplc4.so.0d
%attr(755,root,root) %{_libdir}/%{name}/libplds4.so.0d
%attr(755,root,root) %{_libdir}/%{name}/libnss3.so.1d
%attr(755,root,root) %{_libdir}/%{name}/libnssutil3.so.1d
%attr(755,root,root) %{_libdir}/%{name}/libsmime3.so.1d
%attr(755,root,root) %{_libdir}/%{name}/libssl3.so.1d

# bundle this copy until xdg-utils will have this itself
%attr(755,root,root) %{_libdir}/%{name}/xdg-settings
