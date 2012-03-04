Summary: A collection of extra tools for the Binary Analysis Tool
Name: bat-extratools
Version: 6.0
Release: 1
License: GPLv2, GPLv2+
Source: %{name}-%{version}.tar.gz
Group: Development/Tools
Packager: Armijn Hemel <armijn@binaryanalysis.org>
BuildRequires: xz-devel, lzo-devel, zlib-devel
Requires: lzo, xz-libs, zlib

%description
A collection of extra tools for the Binary Analysis Tool, scraped from GPL source code releases and firmware replacement projects, plus projects.

%prep
%setup -q
%build
make
%install
rm -rf $RPM_BUILD_ROOT
install -D -p -m 755 cramfs/disk-utils/bat-fsck.cramfs $RPM_BUILD_ROOT%{_bindir}/bat-fsck.cramfs
install -D -p -m 755 squashfs4.2/squashfs-tools/bat-unsquashfs42 $RPM_BUILD_ROOT%{_bindir}/bat-unsquashfs42
install -D -p -m 755 squashfs-atheros/squashfs3.3/squashfs-tools/bat-unsquashfs-atheros $RPM_BUILD_ROOT%{_bindir}/bat-unsquashfs-atheros
install -D -p -m 755 squashfs-broadcom/bat-unsquashfs-broadcom $RPM_BUILD_ROOT%{_bindir}/bat-unsquashfs-broadcom
install -D -p -m 755 squashfs-openwrt/bat-unsquashfs-openwrt $RPM_BUILD_ROOT%{_bindir}/bat-unsquashfs-openwrt
install -D -p -m 755 squashfs-ddwrt/bat-unsquashfs-ddwrt $RPM_BUILD_ROOT%{_bindir}/bat-unsquashfs-ddwrt
install -D -p -m 755 squashfs-ralink/squashfs3.2-r2/squashfs-tools/bat-unsquashfs-ralink $RPM_BUILD_ROOT%{_bindir}/bat-unsquashfs-ralink
install -D -p -m 755 squashfs-realtek/squashfs-tools/bat-unsquashfs-realtek $RPM_BUILD_ROOT%{_bindir}/bat-unsquashfs-realtek
install -D -p -m 755 unyaffs/bat-unyaffs $RPM_BUILD_ROOT%{_bindir}/bat-unyaffs
install -D -p -m 755 romfsck/bat-romfsck $RPM_BUILD_ROOT%{_bindir}/bat-romfsck
install -D -p -m 755 code2html-0.9.1/bat-code2html $RPM_BUILD_ROOT%{_bindir}/bat-code2html
%files
%{_bindir}/bat-unsquashfs42
%{_bindir}/bat-unsquashfs-atheros
%{_bindir}/bat-unsquashfs-broadcom
%{_bindir}/bat-unsquashfs-openwrt
%{_bindir}/bat-unsquashfs-ddwrt
%{_bindir}/bat-unsquashfs-ralink
%{_bindir}/bat-unsquashfs-realtek
%{_bindir}/bat-fsck.cramfs
%{_bindir}/bat-unyaffs
%{_bindir}/bat-romfsck
