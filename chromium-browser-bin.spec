# TODO
# - find a way to check for version without having actually to run the browser
#   with a $DISPLAY via about box
%define		svnrev	37391
%define		rel		1
Summary:	A WebKit powered web browser
Name:		chromium-browser-bin
Version:	5.0.308.0
Release:	0.%{svnrev}.%{rel}
License:	BSD, LGPL v2+ (ffmpeg)
Group:		X11/Applications/Networking
# sh get_sources.sh
Source0:	chrome-linux32-r%{svnrev}.zip
# Source0-md5:	f317bb99a9ffd4d966ec127227ad9da0
Source1:	chrome-linux64-r%{svnrev}.zip
# Source1-md5:	110eee27e72ca43cf1199016dc241322
Source2:	chromium-browser.sh
Source3:	chromium-browser.desktop
Source4:	find-lang.sh
Source5:	get_sources.sh
BuildRequires:	rpmbuild(macros) >= 1.453
BuildRequires:	unzip
Requires:	browser-plugins >= 2.0
Requires:	nspr
Requires:	nss
Requires:	xdg-utils
Provides:	wwwbrowser
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		find_lang 	sh find-lang.sh %{buildroot}

%define		_enable_debug_packages	0
%define		no_install_post_strip	1

%define		nss_caps	libfreebl3.so libnss3.so libnssckbi.so libsmime3.so ibsoftokn3.so libssl3.so libnssutil3.so
%define		nspr_caps	libnspr4.so libplc4.so libplds4.so
%define		ffmpeg_caps	libffmpegsumo.so

# list of script capabilities (regexps) not to be used in Provides
%define		_noautoprov	%{nss_caps} %{nspr_caps} %{ffmpeg_caps}
# needs cvs version of libpng, ignore for now
%define		_noautoreq	%{_noautoprov} libpng12.so.0(PNG12_0)

%description
Chromium is an open-source web browser, powered by WebKit.

%prep
%ifarch %{ix86}
%setup -qcT -a0
%endif
%ifarch %{x8664}
%setup -qcT -a1
%endif
%{__sed} -e 's,@localedir@,%{_libdir}/%{name},' %{SOURCE4} > find-lang.sh

mv chrome-linux/product_logo_48.png .
mv chrome-linux/chrome.1 chromium-browser.1
mv chrome-linux/chrome-wrapper .
mv chrome-linux/{chrome,chromium-browser}
chmod a+x chrome-linux/lib*.so*

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name}/plugins,%{_mandir}/man1,%{_pixmapsdir},%{_desktopdir},%{_libdir}/%{name}/themes}

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
%{_libdir}/%{name}/themes
%attr(755,root,root) %{_libdir}/%{name}/chromium-browser

# These unique permissions are intentional and necessary for the sandboxing
%attr(4555,root,root) %{_libdir}/%{name}/chrome_sandbox

# ffmpeg libs
%attr(755,root,root) %{_libdir}/%{name}/libffmpegsumo.so

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
