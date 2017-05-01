Summary:        Fedora package repositories
Name:           fedora-repos
Version:        26
Release:        0.8
License:        MIT
Group:          System Environment/Base
URL:            https://pagure.io/fedora-repos/
# tarball is created by running make archive in the git checkout
Source:         %{name}-%{version}.tar.bz2
Provides:       fedora-repos(%{version})
Requires:       system-release(%{version})
Obsoletes:      fedora-repos-rawhide <= 26-0.5
BuildArch:      noarch

%description
Fedora package repository files for yum and dnf along with gpg public keys

%package rawhide
Summary:        Rawhide repo definitions
Requires:       fedora-repos = %{version}-%{release}
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
for file in fedora*repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done


%files
%defattr(-,root,root,-)
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/fedora.repo
%config(noreplace) /etc/yum.repos.d/fedora-cisco-openh264.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates*.repo
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/*

%files rawhide
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/fedora-rawhide.repo

%changelog
* Mon Mar 02 2017 Mohan Boddu <mboddu@redhat.com> - 26-0.8
- Fix up obsoletes fedora-repos-rawhide versioning

* Mon Feb 27 2017 Mohan Boddu <mboddu@redhat.com> - 26-0.7
- Fix up dependencies

* Mon Feb 27 2017 Mohan Boddu <mboddu@redhat.com> - 26-0.6
- Disable Rawhide
- Enable fedora, updates, updates-testing

* Thu Feb 23 2017 Dennis Gilmore <dennis@ausil.us> - 26-0.5
- add the Fedora 27 key and matching archmap entry

* Mon Sep 26 2016 Dennis Gilmore <dennis@ausil.us> - 26-0.4
- enable gpgcheck on rawhide

* Wed Sep 14 2016 Dennis Gilmore <dennis@ausil.us> - 26-0.3
- fix up baseurl lines
- replace f26 gpg key for wrong uid
- add zypper support rhbz#1373317
- sign aarch64 with primary key

* Mon Aug 08 2016 Dennis Gilmore <dennis@ausil.us> - 26-0.2
- fix up archmap file
- add f26 gpg keys

* Fri Jul 22 2016 Mohan Boddu <mboddu@redhat.com> - 26-0.1
- Setup for rawhide being f26
