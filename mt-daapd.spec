%global username mt-daapd
%global homedir %_var/lib/%username
%global gecos mt-daapd

Summary: An iTunes-compatible media server
Name: mt-daapd
Epoch: 1
Version: 0.2.4.2
Release: 26%{?dist}
License: GPLv2+
Group: Applications/Multimedia
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1: %{name}.service
Patch0: mt-daapd-0.2.4.2-defaults.patch
Patch1: mt-daapd-0.2.4.2-fedora.patch
Url: http://www.fireflymediaserver.org/
BuildRequires:  gcc
BuildRequires: gdbm-devel, avahi-devel, zlib-devel
BuildRequires: flac-devel, libogg-devel, libvorbis-devel
BuildRequires: libid3tag-devel, sqlite-devel
BuildRequires: systemd-units
Requires(pre): shadow-utils
Requires(post): systemd-sysv
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
The purpose of this project is built the best server software to serve
digital music to the Roku Soundbridge and iTunes; to be able to serve
the widest variety of digital music content over the widest range of
devices.

%prep
%setup -q
%patch0 -p1 -b .defaults
%patch1 -p1 -b .fedora

%build
%configure --enable-avahi --enable-oggvorbis --enable-sqlite3 --enable-flac --enable-mdns 
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_localstatedir}/cache/mt-daapd
mkdir -p %{buildroot}%{_localstatedir}/lib/mt-daapd
install %{SOURCE1} %{buildroot}%{_unitdir}/
mkdir -p %{buildroot}%{_sysconfdir}
install -m 0640 contrib/mt-daapd.conf %{buildroot}%{_sysconfdir}/

%pre
getent group %{username} >/dev/null || groupadd -r %{username}
getent passwd %{username} >/dev/null || \
    useradd -r -g %{username} -d %{homedir} -s /sbin/nologin \
    -c '%{gecos}' %{username}
exit 0

%post
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable mt-daapd.service > /dev/null 2>&1 || :
    /bin/systemctl stop mt-daapd.service > /dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart mt-daapd.service >/dev/null 2>&1 || :
fi

%triggerun -- mt-daapd < 0.2.4.2-9
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply mt-daapd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save mt-daapd >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del mt-daapd >/dev/null 2>&1 || :
/bin/systemctl try-restart mt-daapd.service >/dev/null 2>&1 || :

%files
%config(noreplace) %{_sysconfdir}/mt-daapd.conf
%{_sbindir}/mt-daapd
%{_datadir}/mt-daapd
%{_unitdir}/%{name}.service
%attr(0700,mt-daapd,mt-daapd) %{_localstatedir}/cache/mt-daapd
%attr(0700,mt-daapd,mt-daapd) %{_localstatedir}/lib/mt-daapd
%doc AUTHORS COPYING CREDITS NEWS README TODO

%changelog
* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.2.4.2-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.2.4.2-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.2.4.2-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.2.4.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.2.4.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.2.4.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.4.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.4.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.4.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 07 2013 Jean-Francois Saucier <jsaucier@gmail.com> - 1:0.2.4.2-17
- Remove the fixed uid allocation
- Fix the systemd service file to start after remote fs

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.4.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 10 2013 Jon Ciesla <limburgher@gmail.com> - 1:0.2.4.2-15
- Migrate from fedora-usermgmt to guideline scriptlets.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.4.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.4.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.4.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 13 2011 Tom Callaway <spot@fedoraproject.org> - 1:0.2.4.2-11
- improve systemd service (forking, wants avahi, order after avahi)

* Fri Sep 09 2011 Tom Callaway <spot@fedoraproject.org> - 1:0.2.4.2-10
- fix systemd scriptlets

* Thu Sep 08 2011 Tom Callaway <spot@fedoraproject.org> - 1:0.2.4.2-9
- convert to systemd

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.4.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct  2 2010 Mark Chappell <tremble@fedoraproject.org> - 1:0.2.4.2-7
- Remove INSTALL from files list as per package guidelines

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Oct 18 2008 W. Michael Petullo <mike[at]flyn.org> - 0.2.4.2-4
   - Change initscript priority to 98, so that mt-daapd starts after avahi.

* Fri Sep 26 2008 W. Michael Petullo <mike[at]flyn.org> - 0.2.4.2-3
   - Update init script, fix Fedora Bugzilla #461719.

* Thu May 15 2008 W. Michael Petullo <mike[at]flyn.org> - 0.2.4.2-2
   - Bump epoch.

* Wed May 14 2008 W. Michael Petullo <mike[at]flyn.org> - 0.2.4.2-1
   - New upstream version.
   - Remove check-input patch; it's upstream.

* Fri Apr 18 2008 W. Michael Petullo <mike[at]flyn.org> - 0.9-0.2.1696
   - Apply patch by Nico Golde to fix integer overflow, Bugzilla #442688.

* Tue Feb 26 2008 W. Michael Petullo <mike[at]flyn.org> - 0.9-0.1.1696
   - New upstream version.

* Mon Dec 24 2007 W. Michael Petullo <mike[at]flyn.org> - 0.2.4.1-5
   - Change license to GPLv2+.
   - Add requires(post) chkconfig.
   - Change permissions of mt-daapd.playlist.
   - Patch so that service is not enabled by default.

* Thu Dec 20 2007 W. Michael Petullo <mike[at]flyn.org> - 0.2.4.1-4
   - Build with --enable-avahi to avoid Apache / GPL license mix.
   - Build with Vorbis support.
   - Change BuildRequires accordingly.

* Sat Dec 15 2007 W. Michael Petullo <mike[at]flyn.org> - 0.2.4.1-3
   - Fix versions in changelog.
   - Use %%config(noreplace) for config files.   
   - Change group to Applications/Multimedia.
   - Don't chkconfig on.
   - Install mt-daapd.conf chmod 0640.
   - Set proper license.

* Thu Dec 13 2007 W. Michael Petullo <mike[at]flyn.org> - 0.2.4.1-2
   - BuildRequire zlib-devel, which is required for libid3tag-devel.

* Mon Dec 10 2007 W. Michael Petullo <mike[at]flyn.org> - 0.2.4.1-1
   - New upstream verion.

* Sat Jul 21 2007 W. Michael Petullo <mike[at]flyn.org> - 0.2.4-3
   - Own /usr/share/mt-daapd.

* Sun Jul 15 2007 W. Michael Petullo <mike[at]flyn.org> - 0.2.4-2
   - Use directory macros.
   - Don't use %%makeinstall.
   - use cp -P.

* Sat Jul 14 2007 W. Michael Petullo <mike[at]flyn.org> - 0.2.4-1
   - Initial Fedora RPM release candidate.
