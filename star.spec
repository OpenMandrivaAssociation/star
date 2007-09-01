Name:		star
Version:	1.5a84
Release:	%mkrel 1
Summary:	An archiving tool with ACL support
Source:		ftp://ftp.berlios.de/pub/star/alpha/%{name}-%{version}.tar.bz2
License:	GPL
Group:		Archiving/Backup
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	libattr-devel libacl-devel libext2fs-devel
Prefix:		/usr
Patch1:		star_1.5-ren.diff.bz2

%description
Star supports several tar archive formats (including ustar,
GNU tar and new POSIX format). It's faster than other tar
implementations due to advanced buffering.
Star is also the only tar implementation under Linux capable
of archiving Access Control Lists. 

WARNING: The programs smt, and rmt have been renamed in
mt-star and rmt-star to avoid conflicts with GNU tar and mt.

%package devel
Summary:        An archiving tool with ACL devel support
Group:          Archiving/Backup

%description devel
Star supports several tar archive formats (including ustar,
GNU tar and new POSIX format). It's faster than other tar
implementations due to advanced buffering.
Star is also the only tar implementation under Linux capable
of archiving Access Control Lists.

%prep
%setup -q -n star-1.5
%patch1 -p1 -b .rename
# We do not use ext2_fs.h from the glibc library, but from libext2fs2-devel
perl -pi -e 's,<linux/ext2_fs.h>,<ext2fs/ext2_fs.h>,' star/*.c
# lib64 fixes, fed up to file patch
perl -pi -e 's,(INSDIR.+)lib,\1%{_lib},' lib*/*.mk

%build
ln -sf i586-linux-cc.rul RULES/ia64-linux-cc.rul
ln -sf i586-linux-cc.rul RULES/x86_64-linux-cc.rul
ln -sf i586-linux-cc.rul RULES/amd64-linux-cc.rul
ln -sf i686-linux-cc.rul RULES/athlon-linux-cc.rul
perl -pi -e 's,/usr/src/linux/include,,' DEFAULTS/Defaults.linux
perl -pi -e 's,^LDPATH=.*,LDPATH=,' DEFAULTS/Defaults.linux
perl -pi -e 's,^RUNPATH=.*,RUNPATH=,' DEFAULTS/Defaults.linux
perl -pi -e 's,^INS_BASE=.*,INS_BASE=\t\$\(RPM_INSTALLDIR\)\/usr,' DEFAULTS/Defaults.linux
perl -pi -e 's,^INS_KBASE=.*,INS_KBASE=\t\$\(RPM_INSTALLDIR\),' DEFAULTS/Defaults.linux
perl -pi -e 's,bin$,root,' DEFAULTS/Defaults.linux
perl -pi -e "s/^XK_ARCH:=.*/XK_ARCH:=   %{_target_cpu}/" RULES/mk-gmake.id
./Gmake

%install
if [ -d $RPM_BUILD_ROOT ]; then rm -rf $RPM_BUILD_ROOT; fi
./Gmake "INS_BASE=${RPM_BUILD_ROOT}/%{prefix}" install MANDIR=share/man

# The following files conflict with GNU tar & mtr
rm -f ${RPM_BUILD_ROOT}/%{_bindir}/{,us}tar
rm -f ${RPM_BUILD_ROOT}/%{_bindir}/mt
rm -f ${RPM_BUILD_ROOT}/%{_mandir}/man1/match.1
mv ${RPM_BUILD_ROOT}/%{_bindir}/smt ${RPM_BUILD_ROOT}/%{_bindir}/mt-star
mv ${RPM_BUILD_ROOT}/%{_sbindir}/rmt ${RPM_BUILD_ROOT}/%{_sbindir}/rmt-star
mv ${RPM_BUILD_ROOT}/%{_mandir}/man1/rmt.1 ${RPM_BUILD_ROOT}/%{_mandir}/man1/rmt-star.1
# The following devel files conflict with cdrecord
rm -f ${RPM_BUILD_ROOT}/%{_includedir}/avoffset.h
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/libdeflt.a
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/libschily.a
# TODO: To clean:
mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/default
mv ${RPM_BUILD_ROOT}/%{_prefix}%{_sysconfdir}/default/* ${RPM_BUILD_ROOT}/%{_sysconfdir}/default

# fwang: I don't know why it installs to here
rm -f ${RPM_BUILD_ROOT}%{_datadir}/doc/rmt/default-rmt.sample

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc AN-%{version} README COPYING
%doc READMEs/README.linux star/README.*
%doc star/STARvsGNUTAR
%doc rmt/default-rmt.sample
%doc STATUS.alpha TODO
%{_sysconfdir}/default/star
%{_sysconfdir}/default/rmt
%{_bindir}/gnutar
%{_bindir}/tartest
%{_bindir}/mt-star
%{_bindir}/scpio
%{_bindir}/spax
%{_bindir}/star
%{_bindir}/star_sym
%{_bindir}/suntar
%{_sbindir}/rmt-star
%{_mandir}/man1/*.1*

%files devel
%defattr(-,root,root)
%{_includedir}/schily/*.h
%{_includedir}/schily/*/*.h
%{_libdir}/lib*.a
%{_mandir}/man3/*
%{_mandir}/man5/*
