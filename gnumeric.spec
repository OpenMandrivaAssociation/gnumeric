%define _disable_ld_no_undefined 1
%define url_ver %(echo %{version}|cut -d. -f1,2)

%global optflags %{optflags} -Wno-error -Wno-implicit-function-declaration

%define goffice 0.10
%define libname %mklibname spreadsheet %{version}
%define devname %mklibname -d spreadsheet

Summary:	A full-featured spreadsheet for GNOME
Name:		gnumeric
Version:	1.12.59
Release:	1
License:	GPLv2+
Group:		Office
Url:		https://www.gnome.org/projects/gnumeric/
Source0:	https://ftp.gnome.org/pub/GNOME/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
#This patch is borked, leave it here as reference
# configure is disabling gda for now
#Patch1:		gnumeric-1.9.17-format-strings.patch
# (fc) 1.9.3-4mdv fix CVE-2009-0318
#Patch5:		gnumeric-1.8.2-CVE-2009-0318-rh.patch
#Patch6:		gnumeric-1.12.40-workaround-itstool-bug.patch
# https://github.com/GNOME/gnumeric/commit/d0fb2d4454a2865ba4a4a917d04f19b1fb1298d0.patch

BuildRequires:	bison
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtds
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	perl-IO-Compress
BuildRequires:	rarian
BuildRequires:	perl-devel
BuildRequires:	psiconv-devel
BuildRequires:	scrollkeeper
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gmodule-2.0)
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(gthread-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
#BuildRequires:	pkgconfig(libgda-5.0)
BuildRequires:	pkgconfig(libgoffice-0.10)
BuildRequires:	pkgconfig(libgsf-1)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(pangocairo)
BuildRequires:	pkgconfig(pxlib)
BuildRequires:	pkgconfig(pygobject-3.0)
#gw it places files in the versioned goffice directory
# But as usual with the G mess, stuff doesn't make sense and
# goffice's version is 0.9 while its filesystem version is
# 0.10...
Requires:	goffice >= 0.9

%description
This is the Gnumeric, the GNOME spreadsheet program. If you are familiar with 
Excel, you should be ready to use Gnumeric.  It tries to clone all of 
the good features and stay as compatible as possible with Excel in terms of 
usability. Hopefully the bugs have been left behind :).

%files -f %{name}.lang
%doc AUTHORS NEWS BUGS README
%{_bindir}/*
%{_libdir}/goffice/%{goffice}/plugins/gnumeric
%{_libdir}/gnumeric
%{_datadir}/metainfo/org.gnumeric.gnumeric.appdata.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnumeric*.xml
%{_datadir}/gnumeric
%{_datadir}/applications/*
%{_iconsdir}//hicolor/*x*/apps/org.gnumeric.gnumeric.png
%{_mandir}/man1/*

%preun
%preun_uninstall_gconf_schemas %{schemas}

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Spreadsheet library from Gnumeric
Group:		System/Libraries

%description -n %{libname}
This is the Gnumeric, the GNOME spreadsheet program. If you are familiar with 
Excel, you should be ready to use Gnumeric.  It tries to clone all of 
the good features and stay as compatible as possible with Excel in terms of 
usability. Hopefully the bugs have been left behind :).

%files -n %{libname}
%{_libdir}/libspreadsheet-%{version}.so

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Spreadsheet library from Gnumeric - development files
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
This is the Gnumeric, the GNOME spreadsheet program. If you are familiar with 
Excel, you should be ready to use Gnumeric.  It tries to clone all of 
the good features and stay as compatible as possible with Excel in terms of 
usability. Hopefully the bugs have been left behind :).

%files -n %{devname}
%{_libdir}/libspreadsheet.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/libspreadsheet-*/

#----------------------------------------------------------------------------

%prep
%setup -q
%autopatch -p1

%build

#export CC=gcc
%configure

%make_build

%install
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std
rm -vf %{buildroot}%{_datadir}/%{name}/%{version}/perl/*/auto/Gnumeric/.packlist
rm -rf %{buildroot}/var
ln -s %{_datadir}/gnome %{buildroot}%{_datadir}/%{name}/%{version}

desktop-file-install --vendor="" \
	--remove-category="Application" \
	--remove-category="Science" \
	--remove-category="Math" \
	--remove-category="Application" \
	--remove-mime-type="zz-application/zz-winassoc-xls" \
	--add-category="GTK" \
	--add-category="GNOME" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/*

%find_lang %{name} --with-gnome --all-name

