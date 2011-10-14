# NOTES:
# - to look for new tarball, use update-source.sh script
%define		svnrev	105464
%define		rel		1
Summary:	A WebKit powered web browser
Name:		chromium-browser-bin
Version:	16.0.908.0
Release:	%{svnrev}.%{rel}
License:	BSD, LGPL v2+ (ffmpeg)
Group:		X11/Applications/Networking
# sh get_sources.sh
Source0:	chromium-browser32-r%{svnrev}.zip
# NoSourceSource0-md5:	
Source1:	chromium-browser64-r%{svnrev}.zip
# NoSourceSource1-md5:	
NoSource:	0
NoSource:	1
Source2:	chromium-browser.sh
Source3:	chromium-browser.desktop
Source4:	find-lang.sh
Source5:	update-source.sh
BuildRequires:	rpmbuild(macros) >= 1.453
BuildRequires:	unzip
Requires:	browser-plugins >= 2.0
Requires:	libpng12 >= 1:1.2.42-2
Requires:	nspr
Requires:	nss
Requires:	xdg-utils >= 1.0.2-4
Provides:	wwwbrowser
Conflicts:	chromium-browser
Obsoletes:	%{name}-bookmark_manager
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
%define		_noautoreq	%{_noautoprov}

%description
Chromium is an open-source web browser, powered by WebKit.

%package inspector
Summary:	Page inspector for the chromium-browser
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description inspector
Chromium is an open-source browser project that aims to build a safer,
faster, and more stable way for all Internet users to experience the
web.

This package contains 'inspector', allowing web developpers to inspect
any element of a web page at runtime (html, javascript, css, ..)

%package l10n
Summary:	chromium-browser language packages
Group:		I18n
Requires:	%{name} = %{version}-%{release}

%description l10n
Chromium is an open-source browser project that aims to build a safer,
faster, and more stable way for all Internet users to experience the
web.

This package contains language packages for 50 languages:

ar, bg, bn, ca, cs, da, de, el, en-GB, es-419, es, et, fi, fil, fr,
gu, he, hi, hr, hu, id, it, ja, kn, ko, lt, lv, ml, mr, nb, nl, or,
pl, pt-BR, pt-PT, ro, ru, sk, sl, sr, sv, ta, te, th, tr, uk, vi,
zh-CN, zh-TW

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

# xdg-utils >= 1.0.2-4 satisfies these
rm chrome-linux/xdg-settings
rm chrome-linux/xdg-mime

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name}/plugins,%{_mandir}/man1,%{_pixmapsdir},%{_desktopdir},%{_libdir}/%{name}/themes}

install -p %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/chromium-browser
%{__sed} -i -e 's,@libdir@,%{_libdir}/%{name},' $RPM_BUILD_ROOT%{_bindir}/chromium-browser
cp -a chrome-linux/* $RPM_BUILD_ROOT%{_libdir}/%{name}
cp -p chromium-browser.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -p product_logo_48.png $RPM_BUILD_ROOT%{_pixmapsdir}/chromium-browser.png
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}

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
%{__sed} -i -e '/en-US.pak/d' %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_browser_plugins

%postun
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files
%defattr(644,root,root,755)

%{_browserpluginsconfdir}/browsers.d/%{name}.*
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{name}.*.blacklist

%attr(755,root,root) %{_bindir}/chromium-browser
%{_mandir}/man1/chromium-browser.1*
%{_pixmapsdir}/chromium-browser.png
%{_desktopdir}/*.desktop
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/resources.pak
%{_libdir}/%{name}/chrome.pak
%dir %{_libdir}/%{name}/locales
%{_libdir}/%{name}/locales/en-US.pak
%dir %{_libdir}/%{name}/plugins
%dir %{_libdir}/%{name}/resources
%{_libdir}/%{name}/themes
%attr(755,root,root) %{_libdir}/%{name}/chromium-browser

# These unique permissions are intentional and necessary for the sandboxing
%attr(4555,root,root) %{_libdir}/%{name}/chrome_sandbox

# Native Client plugin, to use launch with --enable-nacl
%attr(755,root,root) %{_libdir}/%{name}/libppGoogleNaClPluginChrome.so
#%{_libdir}/%{name}/nacl_irt_x86_64.nexe

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

%files inspector
%defattr(644,root,root,755)
%{_libdir}/%{name}/resources/inspector

%files l10n -f %{name}.lang
%defattr(644,root,root,755)
