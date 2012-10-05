Summary:	A tool to convert True/OpenType fonts to XML and back
Name:		fonttools
Version:	2.3
Release:	1
License:	BSD
Group:		Development/Tools
URL:		http://sourceforge.net/projects/fonttools/
Source0:	http://downloads.sourceforge.net/fonttools/%{name}-%{version}.tar.gz
# Source0-md5:	502cdf6662e1d075f1902fbd995eaace
BuildRequires:	python-devel
BuildRequires:	python-numpy
Requires:	python-numpy
Provides:	ttx = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TTX/FontTools is a tool for manipulating TrueType and OpenType fonts.
It is written in Python and has a BSD-style, open-source license. TTX
can dump TrueType and OpenType fonts to an XML-based text format and
vice versa.

%prep
%setup -q

sed -i.nobang '1 d' Lib/fontTools/ttx.py
chmod a-x LICENSE.txt

%build
CFLAGS="%{rpmcflags} %{rpmcppflags}" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	-O1 \
	--skip-build \
	--root $RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{py_sitedir}/FontTools/fontTools/ttLib/test
chmod 0755 $RPM_BUILD_ROOT%{py_sitedir}/FontTools/fontTools/misc/eexecOp.so

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.txt
%doc Doc/ChangeLog Doc/changes.txt Doc/documentation.html
%{py_sitedir}/FontTools.pth
%dir %{py_sitedir}/FontTools
%dir %{py_sitedir}/FontTools/fontTools
%dir %{py_sitedir}/FontTools/fontTools/encodings
%dir %{py_sitedir}/FontTools/fontTools/misc
%dir %{py_sitedir}/FontTools/fontTools/pens
%dir %{py_sitedir}/FontTools/fontTools/ttLib
%dir %{py_sitedir}/FontTools/fontTools/ttLib/tables
%{py_sitedir}/FontTools/*.py*
%{py_sitedir}/FontTools/fontTools/*.py*
%{py_sitedir}/FontTools/fontTools/*/*.py*
%{py_sitedir}/FontTools/fontTools/*/*/*.py*
%{py_sitedir}/FontTools/fontTools/misc/eexecOp.so
%{py_sitedir}/FontTools/fonttools-%{version}-py?.?.egg-info
%attr(755,root,root) %{_bindir}/ttx
%{_mandir}/man1/ttx.1*
