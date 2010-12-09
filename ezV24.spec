%define name	ezV24
%define version	0.1.1
%define release  %mkrel 6

%define major	0
%define libname %mklibname %{name}_%{major}

Name: 	 	%{name}
Summary: 	Easy to use programming interface for Linux serial ports
Version: 	%{version}
Release: 	%{release}

Source:		lib%{name}-%{version}.tar.bz2
URL:		http://ezv24.sourceforge.net/
License:	GPL
Group:		System/Libraries
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
The goal of this library is to provide an easy to use programming interface to
the serial ports of the Linux system.

%package -n 	%{libname}
Summary:        Dynamic libraries from %name
Group:          System/Libraries
Provides:	%name
Obsoletes:	%name = %version-%release

%description -n %{libname}
Dynamic libraries from %name.

%package -n 	%{libname}-devel
Summary: 	Header files and static libraries from %name
Group: 		Development/C
Requires: 	%{libname} >= %{version}
Provides: 	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release} 
Obsoletes: 	%name-devel

%description -n %{libname}-devel
Libraries and includes files for developing programs based on %name.

%prep
%setup -q -n lib%name-%version
# setup opt flags
perl -p -i -e 's/-O2\ /$RPM_OPT_FLAGS\ /g' Makefile

%build
%make shared
%make static
										
%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %buildroot/%_libdir
install -d -m 755 %buildroot/usr/include/%name
install -m 644 ezV24.h %buildroot/usr/include/%name
install -m 644 -s lib%name-0_s.a %buildroot/%_libdir
install -m 755 -s lib%name.so.0.1 %buildroot/%_libdir
ln -s %_libdir/lib%name.so.0.1 %buildroot/%_libdir/lib%name.so.0
ln -s %_libdir/lib%name.so.0.1 %buildroot/%_libdir/lib%name.so

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc AUTHORS BUGS ChangeLog COPY* HISTORY README
%{_includedir}/%name
%{_libdir}/*.so
%{_libdir}/*.a

