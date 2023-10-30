Summary:         libsoup HTTP client/server library
Name:            libsoup
Version:         2.64.0
Release:         9%{?dist}
License:         GPLv2
URL:             http://wiki.gnome.org/LibSoup
Group:           System Environment/Development
Vendor:          VMware, Inc.
Distribution:    Photon

Source0: http://ftp.gnome.org/pub/GNOME/sources/libsoup/2.57/%{name}-%{version}.tar.xz
%define sha512 %{name}=4ff3d16898bad5481d6abc4a7d2cdccc559e3d2a675128ccb61fba09a39c5c1736aeb7bda77dfd73f97a8660d11e25e88901fb6b957ab47b1e9e8a0fd6740424
Patch0: %{name}-fix-make-check.patch

BuildRequires: glib-devel
BuildRequires: gobject-introspection
BuildRequires: libxml2-devel
BuildRequires: intltool
BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python2-devel
BuildRequires: python2-tools
BuildRequires: glib-networking
BuildRequires: autogen
BuildRequires: sqlite-devel
BuildRequires: libpsl-devel
BuildRequires: krb5-devel
BuildRequires: httpd
BuildRequires: icu-devel

%if 0%{?with_check}
BuildRequires: krb5-devel
%endif

Requires: libxml2
Requires: glib-networking
Requires: libpsl

%description
libsoup is HTTP client/server library for GNOME

%package         devel
Summary:         Header files for libsoup
Group:           System Environment/Development
Requires:        %{name} = %{version}-%{release}
Requires:        libxml2-devel

%description     devel
Header files for libsoup.

%package         doc
Summary:         gtk-doc files for libsoup
Group:           System Environment/Development
Requires:        %{name} = %{version}-%{release}

%description     doc
gtk-doc files for libsoup.

%package         lang
Summary:         Additional language files for libsoup
Group:           System Environment/Development
Requires:        %{name} = %{version}-%{release}

%description     lang
These are the additional language files of libsoup.

%prep
%autosetup -p1

%build
%configure --disable-vala
make %{?_smp_mflags}

%install
rm -rf %{buildroot}%{_infodir}
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%find_lang %{name}

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%exclude %{_libdir}/*.a
%{_libdir}/pkgconfig/*

%files doc
%defattr(-,root,root)
%{_datadir}/gtk-doc/html/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Mon Oct 30 2023 Nitesh Kumar <kunitesh@vmware.com> 2.64.0-9
- Bump version as a part of httpd v2.4.58 upgrade
* Mon Apr 03 2023 Nitesh Kumar <kunitesh@vmware.com> 2.64.0-8
- Bump version as a part of httpd v2.4.56 upgrade
* Mon Jan 30 2023 Nitesh Kumar <kunitesh@vmware.com> 2.64.0-7
- Bump version as a part of httpd v2.4.55 upgrade
* Mon Oct 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.64.0-6
- Remove .la files
* Mon Jun 20 2022 Nitesh Kumar <kunitesh@vmware.com> 2.64.0-5
- Bump version as a part of httpd v2.4.54 upgrade
* Thu Nov 18 2021 Nitesh Kumar <kunitesh@vmware.com> 2.64.0-4
- Version bump up to use libxml2 2.9.11-4.
* Fri Oct 16 2020 Ashwin H <ashwinh@vmware.com> 2.64.0-3
- Bump up to use new icu lib.
* Fri Dec 07 2018 Keerthana <keerthanak@vmware.com> 2.64.0-2
- Fix Make check failures.
* Mon Sep 17 2018 Bo Gan <ganb@vmware.com> 2.64.0-1
- Update to 2.64.0
* Mon Sep 03 2018 Ankit Jain <ankitja@vmware.com> 2.57.1-4
- Fix for CVE-2018-12910
* Mon Jun 18 2018 Tapas Kundu <tkundu@vmware.com> 2.57.1-3
- CVE-2017-2885
* Fri Aug 11 2017 Chang Lee <changlee@vmware.com> 2.57.1-2
- Added krb5-devel to BuildRequires for %check
* Tue Apr 04 2017 Kumar Kaushik <kaushikk@vmware.com> 2.57.1-1
- Upgrading to version 2.57.1
* Fri Nov 18 2016 Alexey Makhalov <amakhalov@vmware.com> 2.53.90-3
- Add sqlite-devel build deps
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.53.90-2
- GA - Bump release of all rpms
* Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> 2.53.90-1
- Updated version.
* Mon Oct 12 2015 Xiaolin Li <xiaolinl@vmware.com> 2.50.0-5
- Moving static lib files to devel package.
* Fri Oct 9 2015 Xiaolin Li <xiaolinl@vmware.com> 2.50.0-4
- Removing la files from packages.
* Mon Jul 20 2015 Divya Thaluru <dthaluru@vmware.com> 2.50.0-3
- Addinf libxml2 to Requires
* Mon Jul 13 2015 Alexey Makhalov <amakhalov@vmware.com> 2.50.0-2
- Exclude /usr/lib/debug
* Fri Jun 5 2015 Touseef Liaqat <tliaqat@vmware.com> 2.50.0-1
- Initial build.  First version
