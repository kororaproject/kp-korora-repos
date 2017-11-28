Summary:        Korora package repositories
Name:           korora-repos
Version:        27
Release:        0.9
License:        MIT
Group:          System Environment/Base
URL:            https://pagure.io/fedora-repos/
# tarball is created by running make archive in the git checkout
Source:         %{name}-%{version}.tar.gz
Provides:       korora-repos(%{version})
Requires:       system-release(%{version})
Obsoletes:      fedora-repos-rawhide <= 25-0.3
Obsoletes:      fedora-repos-anaconda < 22-0.3
Provides:       fedora-repos
Obsoletes:      fedora-repos
BuildArch:      noarch

%description
Korora package repository files for yum and dnf along with gpg public keys

%package rawhide
Summary:        Rawhide repo definitions
Requires:       korora-repos = %{version}-%{release}
Obsoletes:      fedora-release-rawhide <= 22-0.3

%description rawhide
This package provides the rawhide repo definitions.

%prep
%setup -q

%build

%install
# Install the keys
install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 RPM-GPG-KEY* $RPM_BUILD_ROOT/etc/pki/rpm-gpg/

# Link the primary/secondary keys to arch files, according to archmap.
# Ex: if there's a key named RPM-GPG-KEY-fedora-19-primary, and archmap
#     says "fedora-19-primary: i386 x86_64",
#     RPM-GPG-KEY-fedora-19-{i386,x86_64} will be symlinked to that key.
pushd $RPM_BUILD_ROOT/etc/pki/rpm-gpg/
for keyfile in RPM-GPG-KEY*; do
    key=${keyfile#RPM-GPG-KEY-} # e.g. 'fedora-20-primary'
    arches=$(sed -ne "s/^${key}://p" $RPM_BUILD_DIR/%{name}-%{version}/archmap) \
        || echo "WARNING: no archmap entry for $key"
    for arch in $arches; do
        # replace last part with $arch (fedora-20-primary -> fedora-20-$arch)
        ln -s $keyfile ${keyfile%%-*}-$arch # NOTE: RPM replaces %% with %
    done
done
# and add symlink for compat generic location
ln -s RPM-GPG-KEY-fedora-%{version}-primary RPM-GPG-KEY-%{version}-fedora
popd

install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in fedora*repo korora*repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done

# copr config file to enable dnf copr on Korora
install -d -m 755 $RPM_BUILD_ROOT/etc/dnf/plugins
install -m 644 copr.conf $RPM_BUILD_ROOT/etc/dnf/plugins/copr.conf

%files
%defattr(-,root,root,-)
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/fedora.repo
%config(noreplace) /etc/yum.repos.d/fedora-cisco-openh264.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates*.repo
%config(noreplace) /etc/yum.repos.d/korora.repo
%config(noreplace) /etc/dnf/plugins/copr.conf
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/*

%files rawhide
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/fedora-rawhide.repo

%changelog
* Tue Nov 28 2017 Ian Firns <firnsy@kororaproject.org> 27-0.9
- Update for Korora 27

* Mon Jul 31 2017 Ian Firns <firnsy@kororaproject.org> 26-1.0
- Sync'd with distribution-keys package.

* Sun Jul 30 2017 Ian Firns <firnsy@kororaproject.org> 26-0.9
- Disabled updates-testing.

* Wed Jul 19 2017 Ian Firns <firnsy@kororaproject.org> 26-1
- Update for Korora 26

* Thu Sep 01 2016 Chris Smart <csmart@kororaproject.org> 25-1
- Update for Korora 25

* Thu May 12 2016 Chris Smart <csmart@kororaproject.org> 24-1
- Update for Korora 24

* Mon Oct 19 2015 Dennis Gilmore <dennis@ausil.us> - 23-1
- setup for Fedora 23 GA
- disable updates-testing
- set fedora repodata expiry at 28 days
- add all Fedora gpg keys

* Tue Jul 14 2015 Dennis Gilmore <dennis@ausil.us> - 23-0.4
- disable rawhide
- enable fedora, updates, updates-testing

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 23-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 18 2015 Dennis Gilmore <dennis@ausil.us> - 23-0.2
- add the Fedora 23 gpg keys

* Tue Feb 10 2015 Peter Robinson <pbrobinson@fedoraproject.org> 23-0.1
- Setup for f23 rawhide

