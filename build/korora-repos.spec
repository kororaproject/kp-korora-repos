Summary:        Korora package repositories
Name:           korora-repos
Version:        21
Release:        3
License:        MIT
Group:          System Environment/Base
URL:            https://git.fedorahosted.org/cgit/fedora-repos.git/
# tarball is created by running make archive in the git checkout
Source:         %{name}-%{version}.tar.gz
Provides:       korora-repos(%{version})
Requires:       system-release(%{version})
Provides:	fedora-repos
Obsoletes:	fedora-repos
Obsoletes:      fedora-repos-anaconda < 21-1
Obsoletes:      fedora-repos-rawhide < 21-0.4
Obsoletes:      fedora-release-rawhide <= 21-0.7
BuildArch:      noarch

%description
Korora package repository files for yum and dnf along with gpg public keys

%package rawhide
Summary:        Rawhide repo definitions
Requires:       korora-repos = %{version}-%{release}
Obsoletes:      fedora-release-rawhide <= 21-0.7
Obsoletes:      fedora-repos-rawhide

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


%files
%defattr(-,root,root,-)
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/fedora.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates*.repo
%config(noreplace) /etc/yum.repos.d/korora.repo
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/*

%files rawhide
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/fedora-rawhide.repo

%changelog
* Mon Dec 29 2014 Chris Smart <csmart@kororaproject.org> 21-3
- Add Korora 21 GPG keys.

* Sat Nov 22 2014 Dennis Gilmore <dennis@ausil.us> 21-2
- Obsolete fedora-repos-anaconda < 21-1
- due to initial confusion over it some people got it installed

* Tue Nov 18 2014 Dennis Gilmore <dennis@ausil.us> 21-1
- drop no longer needed fedora-repos-anaconda sup-package
- disable updates-testing
- turn on 7 day metadata expire for the fedora repo

* Mon Sep 15 2014 Dennis Gilmore <dennis@ausil.us> 21-0.7
- enable the product repos so anaconda will use them

* Wed Sep 10 2014 Dennis Gilmore <dennis@ausil.us> 21-0.6
- add repo files for the products

* Tue Jul 08 2014 Dennis Gilmore <dennis@ausil.us> 21-0.5
- setup for f21 being branched

* Tue Jul 08 2014 Dennis Gilmore <dennis@ausil.us> 21-0.4
- Require fedora-repos-rawhide from main package
- have fedora-repos-rawhide obsolete fedora-release-rawhide

* Tue Jul 08 2014 Dennis Gilmore <dennis@ausil.us> 21-0.3
- remove %%clean and rm in %%install
- Provides:       fedora-repos(%%{version})
- Requires:       system-release(%%{version})
- change url to git repo
- add note on how to make a tarball

* Tue Jul 08 2014 Dennis Gilmore <dennis@ausil.us> 21-0.2
- use %%{version} not %%{dist_version} in symlink command

* Tue Jul 08 2014 Dennis Gilmore <dennis@ausil.us> 21-0.1
- Initial setup for fedora-repos
