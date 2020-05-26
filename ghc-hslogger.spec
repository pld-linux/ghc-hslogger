#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	hslogger
Summary:	Versatile logging framework for Haskell
Name:		ghc-%{pkgname}
Version:	1.3.1.0
Release:	1
License:	LGPL
Group:		Development/Languages
Source0:	http://hackage.haskell.org/packages/archive/%{pkgname}/%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	4988eed9369f71dda1fba137f5476d9d
Patch0:		ghc-8.10.patch
URL:		http://hackage.haskell.org/package/hslogger/
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-mtl
BuildRequires:	ghc-network >= 2.6
BuildRequires:	ghc-network-bsd >= 2.8.1
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-mtl-prof
BuildRequires:	ghc-network-prof >= 2.6
BuildRequires:	ghc-network-bsd-prof >= 2.8.1
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires:	ghc-mtl
Requires:	ghc-network >= 2.6
Requires:	ghc-network-bsd >= 2.8.1
Obsoletes:	ghc-hslogger-doc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

%description
hslogger is a logging framework for Haskell, roughly similar to
Python's logging module.

hslogger lets each log message have a priority and source be
associated with it. The programmer can then define global handlers
that route or filter messages based on the priority and source.
hslogger also has a syslog handler built in.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-mtl-prof
Requires:	ghc-network-prof >= 2.6
Requires:	ghc-network-bsd-prof >= 2.8.1

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Log
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Log/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Log/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Log/Handler
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Log/Handler/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Log/Handler/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Log/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Log/Handler/*.p_hi
%endif
