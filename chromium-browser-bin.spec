%define		svnver  26865
%define		rel		0.2
Summary:	A WebKit powered web browser
Name:		chromium-browser-bin
Version:	4.0.212.0
Release:	0.%{svnver}.%{rel}
License:	BSD, LGPL v2+ (ffmpeg)
Group:		X11/Applications/Networking
Source0:	http://build.chromium.org/buildbot/snapshots/chromium-rel-linux-64/%{svnver}/chrome-linux.zip
# NoSource0-md5:	e071fd30aa2de0eec10bcf5e16ca917b
NoSource:	0
Source2:	chromium-browser.sh
Source3:	chromium-browser.desktop
Source4:	find-lang.sh
Requires:	browser-plugins >= 2.0
Requires:	nspr
Requires:	nss
Provides:	wwwbrowser
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		find_lang 	sh find-lang.sh %{buildroot}

%define		_enable_debug_packages	0

%define		nss_caps	libfreebl3.so libnss3.so libnssckbi.so libsmime3.so ibsoftokn3.so libssl3.so libnssutil3.so
%define		nspr_caps	libnspr4.so libplc4.so libplds4.so

# list of script capabilities (regexps) not to be used in Provides
%define		_noautoprov		%{nss_caps} %{nspr_caps}
%define		_noautoreq		%{_noautoprov}

%description
Chromium is an open-source web browser, powered by WebKit.

%prep
%setup -qc
%{__sed} -e 's,@localedir@,%{_libdir}/%{name},' %{SOURCE4} > find-lang.sh

mv chrome-linux/product_logo_48.png .
mv chrome-linux/xdg-settings .
mv chrome-linux/chromium-browser.1 .
mv chrome-linux/chrome-wrapper .
mv chrome-linux/{chrome,chromium-browser}
chmod a+x chrome-linux/lib*.so*

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name},%{_mandir}/man1,%{_pixmapsdir},%{_desktopdir}}

install -p %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/chromium-browser
%{__sed} -i -e 's,@libdir@,%{_libdir}/%{name},' $RPM_BUILD_ROOT%{_bindir}/chromium-browser
cp -a chrome-linux/* $RPM_BUILD_ROOT%{_libdir}/%{name}
cp -a chromium-browser.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -a product_logo_48.png $RPM_BUILD_ROOT%{_pixmapsdir}/chromium-browser.png
cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}

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

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/chromium-browser
%{_mandir}/man1/chromium-browser.1*
%{_pixmapsdir}/chromium-browser.png
%{_desktopdir}/*.desktop
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/chrome.pak
%dir %{_libdir}/%{name}/locales
%{_libdir}/%{name}/resources
%{_libdir}/%{name}/themes
%attr(755,root,root) %{_libdir}/%{name}/chromium-browser
# These unique permissions are intentional and necessary for the sandboxing
%attr(4555,root,root) %{_libdir}/%{name}/chrome_sandbox

# ffmpeg libs
%attr(755,root,root) %{_libdir}/chromium-browser-bin/libavcodec.so.52
%attr(755,root,root) %{_libdir}/chromium-browser-bin/libavformat.so.52
%attr(755,root,root) %{_libdir}/chromium-browser-bin/libavutil.so.50

# nspr/nss symlinks
%attr(755,root,root) %{_libdir}/chromium-browser-bin/libnspr4.so.0d
%attr(755,root,root) %{_libdir}/chromium-browser-bin/libplc4.so.0d
%attr(755,root,root) %{_libdir}/chromium-browser-bin/libplds4.so.0d
%attr(755,root,root) %{_libdir}/chromium-browser-bin/libnss3.so.1d
%attr(755,root,root) %{_libdir}/chromium-browser-bin/libnssutil3.so.1d
%attr(755,root,root) %{_libdir}/chromium-browser-bin/libsmime3.so.1d
%attr(755,root,root) %{_libdir}/chromium-browser-bin/libssl3.so.1d
