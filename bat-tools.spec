Summary: A collection of extra tools for the Binary Analysis Tool
Name: bat-extratools
Version: 1.0
Release: 1
License: GPLv2 and GPLv2+
Source: %{name}-%{version}.tar.gz
Group: Development/Tools
Packager: Armijn Hemel <armijn@binaryanalysis.org>
BuildRequires: xz-devel, lzo-devel

%description
A collection of extra tools for the Binary Analysis Tool, scraped from GPL source code releases and firmware replacement projects.

%prep
%setup -q
%build
make
%install
rm -rf $RPM_BUILD_ROOT
install -D -p -m 755 squashfs-broadcom/unsquashfs $RPM_BUILD_ROOT%{_bindir}/bat-unsquashfs-broadcom
install -D -p -m 755 squashfs-openwrt/unsquashfs-lzma $RPM_BUILD_ROOT%{_bindir}/bat-unsquashfs-openwrt
install -D -p -m 755 squashfs4.2/squashfs-tools/unsquashfs $RPM_BUILD_ROOT%{_bindir}/bat-unsquashfs42
install -D -p -m 755 squashfs-ralink/squashfs3.2-r2/squashfs-tools/unsquashfs $RPM_BUILD_ROOT%{_bindir}/bat-unsquashfs-ralink
install -D -p -m 755 cramfs/disk-utils/fsck.cramfs $RPM_BUILD_ROOT%{_bindir}/bat-fsck.cramfs
install -D -p -m 755 unyaffs/unyaffs $RPM_BUILD_ROOT%{_bindir}/bat-unyaffs
%files
%{_bindir}/bat-unsquashfs-broadcom
%{_bindir}/bat-unsquashfs-openwrt
%{_bindir}/bat-unsquashfs-ralink
%{_bindir}/bat-unsquashfs42
%{_bindir}/bat-fsck.cramfs
%{_bindir}/bat-unyaffs
