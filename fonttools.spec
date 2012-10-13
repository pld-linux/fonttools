Summary:	A tool to convert TrueType/OpenType fonts to XML and back
Summary(pl.UTF-8):	Narzędzie do konwersji fontów TrueType/OpenType do/z XML-a
Name:		fonttools
Version:	2.3
Release:	1
License:	BSD
Group:		Development/Tools
Source0:	http://downloads.sourceforge.net/fonttools/%{name}-%{version}.tar.gz
# Source0-md5:	502cdf6662e1d075f1902fbd995eaace
URL:		http://sourceforge.net/projects/fonttools/
BuildRequires:	python-devel
BuildRequires:	python-numpy
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
Requires:	python-numpy
Provides:	ttx = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TTX/FontTools is a tool for manipulating TrueType and OpenType fonts.
It is written in Python and has a BSD-style, open-source license. TTX
can dump TrueType and OpenType fonts to an XML-based text format and
vice versa.

%description -l pl.UTF-8
TTX/FontTools to narzędzie do operacji na fontach TrueType i OpenType.
Zostało napisane w Pythonie i ma otwartą licencję w stylu BSD. TTX
potrafi wykonywać zrzuty fontów TrueType i OpenType do formatu
tekstowego opartego na XML-u oraz dokonać operacji odwrotnej.

%prep
%setup -q

%{__sed} -i.nobang '1 d' Lib/fontTools/ttx.py
chmod a-x LICENSE.txt

%build
CFLAGS="%{rpmcflags} %{rpmcppflags}" \
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT

%{__python} setup.py install \
	-O1 \
	--skip-build \
	--root $RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/FontTools/fontTools/ttLib/test
chmod 755 $RPM_BUILD_ROOT%{py_sitedir}/FontTools/fontTools/misc/eexecOp.so
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.txt Doc/{ChangeLog,changes.txt,documentation.html}
%attr(755,root,root) %{_bindir}/ttx
%{py_sitedir}/FontTools.pth
%dir %{py_sitedir}/FontTools
%{py_sitedir}/FontTools/*.py[co]
%dir %{py_sitedir}/FontTools/fontTools
%{py_sitedir}/FontTools/fontTools/*.py[co]
%{py_sitedir}/FontTools/fontTools/encodings
%dir %{py_sitedir}/FontTools/fontTools/misc
%{py_sitedir}/FontTools/fontTools/misc/*.py[co]
%attr(755,root,root) %{py_sitedir}/FontTools/fontTools/misc/eexecOp.so
%{py_sitedir}/FontTools/fontTools/pens
%{py_sitedir}/FontTools/fontTools/ttLib
%{py_sitedir}/FontTools/fonttools-%{version}-py*.egg-info
%{_mandir}/man1/ttx.1*
