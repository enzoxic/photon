Summary:        Library for talking to WWAN modems and devices
Name:           libqmi
Version:        1.26.10
Release:        1%{?dist}
URL:            https://www.freedesktop.org
License:        GPLv2
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://www.freedesktop.org/software/libqmi/libqmi-%{version}.tar.xz
%define sha512 %{name}=48e15b6510437068498657045d21b5481458914e5021b41c372b5d59d51a182a947c6ab3fd06f59888bc9bf09ead4b363ec0a5620f006c89e09bbe915d7daab3

BuildRequires:  libmbim-devel
BuildRequires:  libgudev-devel
BuildRequires:  systemd-devel
BuildRequires:  systemd-libs
BuildRequires:  gcc
BuildRequires:  pkg-config
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool

Requires:       libmbim
Requires:       libgudev

Patch0:         Fix-swi-get-status-ready.patch

%description
The libqmi package contains a GLib-based library for talking to WWAN modems
and devices which speak the Qualcomm MSM Interface (QMI) protocol.

%package        devel
Summary:        Header and development files for libqmi
Requires:       %{name} = %{version}
Requires:       libmbim-devel
%description    devel
It contains the libraries and header files for libqmi

%prep
%autosetup -p1

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
%if 0%{?with_check}
make %{?_smp_mflags} check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libexecdir}/qmi-proxy
%{_bindir}/qmicli
%{_bindir}/qmi-network
%{_bindir}/qmi-firmware-update
%{_libdir}/libqmi-glib.so*
%exclude %dir %{_libdir}/debug
%{_mandir}/man1/*
%{_datadir}/bash-completion/*

%files devel
%defattr(-,root,root)
%{_includedir}/libqmi-glib/*
%{_libdir}/pkgconfig/qmi-glib.pc
%{_datadir}/gtk-doc/*

%changelog
* Wed Dec 20 2023 Mukul Sikka <msikka@vmware.com> 1.26.10-1
- Package update to fix pkg-tests
* Tue Mar 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.26.4-3
- Exclude debug symbols properly
* Mon Dec 14 2020 Susant Sahani <ssahani@vmware.com> 1.26.4-2
- Add build requires
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 1.26.4-1
- Automatic Version Bump
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.26.2-1
- Automatic Version Bump
* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.20.2-1
- Initial build. First version
