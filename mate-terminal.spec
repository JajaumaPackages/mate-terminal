# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.16

# Settings used for build from snapshots.
%{!?rel_build:%global commit ac33ed09bb41ba717df3722cc71e25c1aa5134c5}
%{!?rel_build:%global commit_date 20150709}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Summary:        Terminal emulator for MATE
Name:           mate-terminal
Version:        %{branch}.0
%if 0%{?rel_build}
Release:        2%{?dist}
%else
Release:        0.2%{?git_rel}%{?dist}
%endif
License:        GPLv3+
URL:            http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R mate-terminal.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

#Default to black bg white fg, unlimited scrollback, turn off use theme default
Patch0:        mate-terminal_better_defaults-1.15.1.patch
# fix rhbz (#1377805)
# https://github.com/mate-desktop/mate-terminal/pull/142
Patch1:        mate-terminal_0003-fix-position-with-geometry-option.patch

BuildRequires: dconf-devel
BuildRequires: desktop-file-utils
BuildRequires: glib2-devel
BuildRequires: gtk3-devel
BuildRequires: libSM-devel
BuildRequires: mate-common
BuildRequires: vte291-devel

# needed to get a gsettings schema, rhbz #908105
Requires:      mate-desktop-libs
Requires:      gsettings-desktop-schemas

%description
Mate-terminal is a terminal emulator for MATE. It supports translucent
backgrounds, opening multiple terminals in a single window (tabs) and
clickable URLs.

%prep
%setup -q%{!?rel_build:n %{name}-%{commit}}

%patch0 -p1 -b .better_defaults
%patch1 -p1 -b .fix-position

%if 0%{?rel_build}
#NOCONFIGURE=1 ./autogen.sh
%else # 0%{?rel_build}
# needed for git snapshots
NOCONFIGURE=1 ./autogen.sh
%endif # 0%{?rel_build}

%build
%configure --disable-static                \
           --disable-schemas-compile       

make %{?_smp_mflags} V=1


%install
%{make_install}

desktop-file-install                                                    \
        --delete-original                                               \
        --dir=%{buildroot}%{_datadir}/applications                      \
%{buildroot}%{_datadir}/applications/mate-terminal.desktop

%find_lang %{name} --with-gnome --all-name


%postun
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README ChangeLog
%{_bindir}/mate-terminal
%{_bindir}/mate-terminal.wrapper
%{_datadir}/mate-terminal/
%{_datadir}/applications/mate-terminal.desktop
%{_datadir}/glib-2.0/schemas/org.mate.terminal.gschema.xml
%{_datadir}/appdata/mate-terminal.appdata.xml
%{_mandir}/man1/*


%changelog
* Wed Sep 21 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.16.0-2
- fix rhbz (#1377805)
- fix terminal window position with geometry option

* Wed Sep 21 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.16.0-1
- update to 1.16.0 release

* Wed Sep 07 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.1-2
- fix rhbz (#1357693)

* Fri Jul 22 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.1-1
- update to 1.15.1 release

* Thu Jun 09 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.0-1
- update to 1.15.0 release

* Thu May 26 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.14.0-2
- switch to gtk3
- https://github.com/mate-desktop/mate-terminal/pull/118

* Thu Apr 07 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.14.0-1
- update to 1.14.0

* Fri Mar 11 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.13.2-1
- update to 1.13.2 release

* Mon Feb 22 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.13.1-1
- update to 1.13.1 release

* Sun Feb 07 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.13.0-1
- update to 1.13.0 release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 04 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.1-1
- update to 1.12.1 release

* Fri Nov 06 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.0-1
- update to 1.12.0 release

* Thu Oct 22 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.11.0-1
- update to 1.11.0 release
- remove upstreamed patch

* Thu Oct 01 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.1-2
- fix usage of --tab at command line

* Sat Jul 11 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.1-1
- update to 1.10.1 release
- remove upstreamed patches

* Fri Jul 03 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-3
- use old help from 1.8

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 10 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-1
- update to 1.10.0 release

* Wed May 06 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.91-1
- update to 1.9.91 release

* Mon Apr 06 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.90-11
- update to 1.9.90 release

* Thu Jan 22 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.1-1
- update to 1.9.1 release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.0-1
- update to 1.9.0 release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Wed Feb 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.2-1
- Update to 1.7.2

* Sat Jan 18 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-1
- update to 1.7.1 release
- remove obsolete configure flags
- clean up BR's
- use modern 'make install' macro
- add --with-gnome --all-name for find language
- clean up file section

* Fri Dec 06 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Thu Aug 08 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-11
- switch to runtime require mate-desktop-libs, fix rhbz #908105

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1.9
- another fix for better default patch

* Sat Jun 29 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1.8
- add runtime require gsettings-desktop-schemas to have proxy support
- from gnome gsettings schema

* Fri Jun 28 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1.7
- improve better_default patch
- remove BR gsettings-desktop-schemas-devel
- remove update-desktop-database scriptlet

* Mon Jun 17 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-6
- Update patch for bold colors

* Fri May 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-5
- Update patch again

* Fri May 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-4
- Update patch (again) to really fix annoying default settings

* Fri May 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-3
- Update patch to really fix annoying default settings
- New defaults: unlimited scrollback black bg

* Fri May 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-2
- Add patch to fix annoying default settings

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-1
- Bugfix release. See Cangelog.

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to stable 1.6.0 release

* Tue Mar 26 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-1
- Update to latest upstream release

* Mon Feb 18 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.0-3
- Add hard requires for mate-desktop to fix RHBZ #908105

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 19 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.0-1
- Update to latest upstream release
- Special thanks to Shawn Sterling for his help

* Wed Oct 24 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-4
- Add requires libmate

* Mon Oct 15 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-3
- add build requires rarian-compat

* Mon Oct 15 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-2
- remove surplus build requires

* Sun Oct 14 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-1
- initial build
