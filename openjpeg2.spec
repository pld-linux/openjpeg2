#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	An open-source JPEG 2000 codec
Summary(pl.UTF-8):	Biblioteka kodująca i dekodująca format JPEG 2000
Name:		openjpeg2
Version:	2.3.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/uclouvain/openjpeg/releases/
Source0:	https://github.com/uclouvain/openjpeg/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	6a1f8aaa1fe55d2088e3a9c942e0f698
URL:		http://www.openjpeg.org/
BuildRequires:	cmake >= 2.8.2
BuildRequires:	doxygen
BuildRequires:	lcms2-devel >= 2
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	pkgconfig >= 1:0.22
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The OpenJPEG 2 library is an open-source JPEG 2000 codec written in C
language. It has been developed in order to promote the use of JPEG
2000, the new still-image compression standard from the Joint
Photographic Experts Group (JPEG).

%description -l pl.UTF-8
OpenJPEG 2 to mająca otwarte źródła biblioteka kodująca i dekodująca
format JPEG 2000, napisana w języku C. Powstała w celu promowania
użycia formatu JPEG 2000 - nowego standardu obrazów nieruchomych
stworzonego przez grupę JPEG (Joint Photographic Experts Group).

%package devel
Summary:	Header file for OpenJPEG 2 library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki OpenJPEG 2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header file needed for developing programs
using the OpenJPEG 2 library.

%description devel -l pl.UTF-8
Ten pakiet zawiera plik nagłówkowy potrzebny do tworzenia programów
wykorzystujących bibliotekę OpenJPEG 2.

%package static
Summary:	Static OpenJPEG 2 library
Summary(pl.UTF-8):	Statyczna biblioteka OpenJPEG 2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OpenJPEG 2 library.

%description static -l pl.UTF-8
Statyczna biblioteka OpenJPEG 2.

%package progs
Summary:	OpenJPEG 2 codec programs
Summary(pl.UTF-8):	Programy kodujące/dekodujące dla biblioteki OpenJPEG 2
Group:		Applications/Graphics
Requires:	%{name} = %{version}-%{release}

%description progs
OpenJPEG 2 codec programs.

%description progs -l pl.UTF-8
Programy kodujące/dekodujące dla biblioteki OpenJPEG 2.

%prep
%setup -q -n openjpeg-%{version}

%build
%cmake . \
	-DBUILD_DOC=ON \
	%{!?with_static_libs:-DBUILD_STATIC_LIBS=OFF} \
	-DOPENJPEG_INSTALL_LIB_DIR=%{_lib}

# not ready for openjpeg 2:
#	-DBUILD_JAVA=ON
#	-DBUILD_JPWL=ON
#	-DBUILD_MJ2=ON
#	-DBUILD_VIEWER=ON -DwxWidgets_CONFIG_EXECUTABLE=/usr/bin/wx-gtk2-unicode-config

# no BUILD_JPIP here (see openjpip.spec for it)
# no BUILD_JP3D here (see openjp3d.spec for it)

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/openjpeg-2.3
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/html

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS.md CHANGELOG.md LICENSE NEWS.md README.md THANKS.md
%attr(755,root,root) %{_libdir}/libopenjp2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopenjp2.so.7

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopenjp2.so
%{_includedir}/openjpeg-2.3
%dir %{_libdir}/openjpeg-2.3
%{_libdir}/openjpeg-2.3/OpenJPEG*.cmake
%{_pkgconfigdir}/libopenjp2.pc
%{_mandir}/man3/libopenjp2.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopenjp2.a
%endif

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/opj_compress
%attr(755,root,root) %{_bindir}/opj_decompress
%attr(755,root,root) %{_bindir}/opj_dump
%{_mandir}/man1/opj_compress.1*
%{_mandir}/man1/opj_decompress.1*
%{_mandir}/man1/opj_dump.1*
