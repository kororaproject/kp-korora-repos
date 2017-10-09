Summary:        Fedora package repositories
Name:           fedora-repos
Version:        27
Release:        0.6%{?_module_build:%{?dist}}
License:        MIT
Group:          System Environment/Base
URL:            https://pagure.io/fedora-repos/
# tarball is created by running make archive in the git checkout
Source:         %{name}-%{version}.tar.bz2
Provides:       fedora-repos(%{version})
Requires:       system-release(%{version})
Requires:       fedora-gpg-keys = %{version}-%{release}
Obsoletes:      fedora-repos-rawhide <= 27-0.4
Obsoletes:      fedora-repos-anaconda < 22-0.3
BuildArch:      noarch

%description
Fedora package repository files for yum and dnf along with gpg public keys

%package rawhide
Summary:        Rawhide repo definitions
Requires:       fedora-repos = %{version}-%{release}
Obsoletes:      fedora-release-rawhide <= 22-0.3

%description rawhide
This package provides the rawhide repo definitions.

%package -n fedora-gpg-keys
Summary:        Fedora RPM keys
Obsoletes:      fedora-release-rawhide <= 22-0.3

%description -n fedora-gpg-keys
This package provides the RPM signature keys.

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
for file in fedora*repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done


%files
%defattr(-,root,root,-)
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/fedora.repo
%config(noreplace) /etc/yum.repos.d/fedora-cisco-openh264.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates*.repo

%files rawhide
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/fedora-rawhide.repo

%files -n fedora-gpg-keys
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/*

%changelog
* Mon Sep 25 2017 Stephen Gallagher <sgallagh@redhat.com> - 27-0.6
- Add a dist tag when building for modules

* Fri Sep 22 2017 Patrick Uiterwijk <patrick@puiterwijk.org> - 27-0.5
- Do not require rawhide, but obsolete it

* Fri Sep 22 2017 Patrick Uiterwijk <patrick@puiterwijk.org> - 27-0.4
- Split out GPG keys into fedora-gpg-keys

* Tue Aug 15 2017 Dennis Gilmore <dennis@ausil.us> - 27-0.3
- Disable Rawhide
- Enable fedora, updates, updates-testing
- Add Fedora 28 key

* Tue May 16 2017 Dennis Gilmore <dennis@ausil.us> - 27-0.2
- add the missing Fedora 14 secondary arch key
- add the new modularity key

* Sat Feb 25 2017 Mohan Boddu <mboddu@redhat.com> - 27-0.1
- Setup for rawhide being f27
