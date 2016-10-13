%define debug_package %{nil}

%define mybuildnumber %{?build_number}%{?!build_number:1}

Name:           qubes-vpn
Version:        0.0.2
Release:        %{mybuildnumber}%{?dist}
Summary:        Leakproof VPN for your Qubes OS ProxyVMs
BuildArch:      noarch

License:        GPLv3+
URL:            https://github.com/Rudd-O/qubes-vpn
Source0:	Source0: https://github.com/Rudd-O/%{name}/archive/{%version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  sed
Requires: openvpn
Requires: iptables
Requires: /sbin/ip
Requires: /sbin/sysctl
Requires: qubes-db
Requires: util-linux
Requires: ipcalc
Requires: sudo
Requires: coreutils
Requires: libnotify
Requires: gawk

%description
This package lets you setup an OpenVPN-based leakproof VPN on Qubes OS.

%prep
%setup -q

%build
# variables must be kept in sync with install
make DESTDIR=$RPM_BUILD_ROOT SBINDIR=%{_sbindir} BINDIR=%{_bindir} UNITDIR=%{_unitdir} PRESETDIR=%{_prefix}/lib/systemd/system-preset/ SYSCONFDIR=%{_sysconfdir}

%install
rm -rf $RPM_BUILD_ROOT
# variables must be kept in sync with build
make install DESTDIR=$RPM_BUILD_ROOT SBINDIR=%{_sbindir} BINDIR=%{_bindir} UNITDIR=%{_unitdir} PRESETDIR=%{_prefix}/lib/systemd/system-preset/ SYSCONFDIR=%{_sysconfdir}

%files
%attr(0755, root, root) %{_sbindir}/qubes-vpn*
%attr(0755, root, root) %{_bindir}/qubes-vpn*
%attr(0644, root, root) %{_unitdir}/qubes-vpn*
%attr(0644, root, root) %{_prefix}/lib/systemd/system-preset/*qubes-vpn*
%attr(0440, root, root) %{_sysconfdir}/sudoers.d/qubes-vpn
%attr(0644, root, root)%{_sysconfdir}/xdg/autostart/qubes-vpn-notifier.desktop
%doc README.md

%pre
getent group qubes-vpn >/dev/null || groupadd -r qubes-vpn || :
getent passwd qubes-vpn >/dev/null || \
  useradd -c "Privilege-separated Qubes VPN" -g qubes-vpn \
  -s /sbin/nologin -r -d /var/empty/qubes-vpn qubes-vpn 2> /dev/null || :

%post
%systemd_post qubes-vpn.service qubes-vpn-forwarding.service

%preun
%systemd_preun qubes-vpn.service qubes-vpn-forwarding.service

%changelog
* Wed Oct 12 2016 Manuel Amador (Rudd-O) <rudd-o@rudd-o.com>
- Initial release