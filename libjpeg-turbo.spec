Name:		libjpeg-turbo
Version:	1.2.1
Release:	1%{?dist}
Summary:	A MMX/SSE2 accelerated library for manipulating JPEG image files

Group:		System Environment/Libraries
License:	wxWidgets
URL:		http://sourceforge.net/projects/libjpeg-turbo
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	autoconf, automake, libtool
%ifarch %{ix86} x86_64
BuildRequires:	nasm
%endif

Obsoletes:	libjpeg < 6b-47
# add provides (even if it not needed) to workaround bad packages, like
# java-1.6.0-openjdk (#rh607554) -- atkac
Provides:	libjpeg = 6b-47%{?dist}
%if "%{?_isa}" != ""
Provides:	libjpeg%{_isa} = 6b-47%{?dist}
%endif

Patch0:		libjpeg-turbo12-noinst.patch

%description
The libjpeg-turbo package contains a library of functions for manipulating
JPEG images. It also contains simple client programs for
accessing the libjpeg functions. It contains cjpeg, djpeg, jpegtran,
rdjpgcom and wrjpgcom. Cjpeg compresses an image file into JPEG format.
Djpeg decompresses a JPEG file into a regular image file. Jpegtran
can perform various useful transformations on JPEG files. Rdjpgcom
displays any text comments included in a JPEG file. Wrjpgcom inserts
text comments into a JPEG file.

%package devel
Summary:	Headers for the libjpeg-turbo library
Group:		Development/Libraries
Obsoletes:	libjpeg-devel < 6b-47
Provides:	libjpeg-devel = 6b-47%{?dist}
%if "%{?_isa}" != ""
Provides:	libjpeg-devel%{_isa} = 6b-47%{?dist}
%endif
Requires:	libjpeg-turbo%{?_isa} = %{version}-%{release}

%description devel
This package contains header files necessary for developing programs which
will manipulate JPEG files using the libjpeg-turbo library.

%package static
Summary:	Static version of the libjpeg-turbo library
Group:		Development/Libraries
Obsoletes:	libjpeg-static < 6b-47
Provides:	libjpeg-static = 6b-47%{?dist}
%if "%{?_isa}" != ""
Provides:	libjpeg-static%{_isa} = 6b-47%{?dist}
%endif
Requires:	libjpeg-turbo-devel%{?_isa} = %{version}-%{release}

%description static
The libjpeg-turbo-static package contains a static library for manipulating
JPEG images.

%prep
%setup -q

%patch0 -p1 -b .noinst

%build
autoreconf -fiv

%configure

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Fix perms
chmod -x README-turbo.txt

# Remove unwanted .la files
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

# Don't distribute libturbojpeg, for now
rm -f $RPM_BUILD_ROOT/%{_libdir}/libturbojpeg.*
rm -f $RPM_BUILD_ROOT/%{_includedir}/turbojpeg.h

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README README-turbo.txt change.log ChangeLog.txt
%doc usage.txt wizard.txt
%{_libdir}/libjpeg.so.62.0.0
%{_libdir}/libjpeg.so.62
%{_bindir}/cjpeg
%{_bindir}/djpeg
%{_bindir}/jpegtran
%{_bindir}/rdjpgcom
%{_bindir}/wrjpgcom
%{_mandir}/man1/cjpeg.1*
%{_mandir}/man1/djpeg.1*
%{_mandir}/man1/jpegtran.1*
%{_mandir}/man1/rdjpgcom.1*
%{_mandir}/man1/wrjpgcom.1*

%files devel
%defattr(-,root,root,-)
%doc coderules.txt jconfig.txt libjpeg.txt structure.txt example.c
%{_includedir}/jconfig.h
%{_includedir}/jerror.h
%{_includedir}/jmorecfg.h
%{_includedir}/jpeglib.h
%{_libdir}/libjpeg.so

%files static
%defattr(-,root,root,-)
%{_libdir}/libjpeg.a

%changelog
* Mon Oct  1 2012 Tom Lane <tgl@redhat.com> 1.2.1-1
- Imported into RHEL-6 from Fedora 18
- Dropped separate utils subpackage, because existing packages might expect
  that Requires: libjpeg is enough to pull in the command-line tools;
  we should only alter the subpackage breakdown in a new RHEL branch
- Dropped turbojpeg build, because it doesn't seem ready for prime time
  and isn't part of our RHEL-6 requirements anyway
Resolves: #788687
