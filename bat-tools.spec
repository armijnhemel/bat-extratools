Summary: A collection of extra tools for the Binary Analysis Tool
Name: bat-extratools
Version: 1.0
Release: 1
License: GPLv2+
Source: %{name}-%{version}.tar.gz
Group: Development/Tools
Packager: Armijn Hemel <armijn@binaryanalysis.org>

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
install -D -p -m 755 cramfs/disk-utils/fsck.cramfs $RPM_BUILD_ROOT%{_bindir}/bat-fsck.cramfs
%files
%{_bindir}/bat-unsquashfs-broadcom
%{_bindir}/bat-unsquashfs-openwrt
%{_bindir}/bat-fsck.cramfs
