#
# Conditional build:
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# pytest tests

Summary:	A tool to convert TrueType/OpenType fonts to XML and back
Summary(pl.UTF-8):	Narzędzie do konwersji fontów TrueType/OpenType do/z XML-a
Name:		fonttools
Version:	3.44.0
Release:	4
# basic license is BSD
# FontTools includes Adobe AGL & AGLFN, which is under 3-clauses BSD license
License:	MIT, BSD
Group:		Development/Tools
#Source0Download: https://github.com/fonttools/fonttools/releases
Source0:	https://github.com/fonttools/fonttools/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	3f9ff311081a0f591a09552902671d29
URL:		https://github.com/fonttools/fonttools
%if %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-enum34 >= 1.1.6
BuildRequires:	python-fs >= 2.2.0
BuildRequires:	python-pytest >= 3.0
BuildRequires:	python-unicodedata2 >= 12.0.0
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.4
%if %{with tests}
BuildRequires:	python3-fs >= 2.2.0
BuildRequires:	python3-pytest >= 3.0
%if "%{py3_ver}" < "3.7"
BuildRequires:	python3-unicodedata2 >= 12.0.0
%endif
%endif
%endif
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3 >= 1.5.5
%endif
%if %{with python2}
Requires:	python-fonttools = %{version}-%{release}
Requires:	python-setuptools
%else
Requires:	python3-fonttools = %{version}-%{release}
Requires:	python3-setuptools
%endif
Provides:	ttx = %{version}-%{release}
BuildArch:	noarch
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

%package -n python-fonttools
Summary:	Python 2 tools to manipulate font files
Summary(pl.UTF-8):	Narzędzia do manipulacji na plikach fontów dla Pythona 2
Group:		Libraries/Python
Requires:	python-modules >= 1:2.7
Requires:	python-unicodedata2 >= 11.0.0

%description -n python-fonttools
Python 2 tools to manipulate font files.

%description -n python-fonttools -l pl.UTF-8
Narzędzia do manipulacji na plikach fontów dla Pythona 2.

%package -n python-fonttools-apidocs
Summary:	Documentation for Python fonttools module
Summary(pl.UTF-8):	Dokumentacja modułu Pythona fonttools
Group:		Documentation

%description -n python-fonttools-apidocs
Documentation for Python fonttools module.

%description -n python-fonttools-apidocs -l pl.UTF-8
Dokumentacja modułu Pythona fonttools.

%package -n python3-fonttools
Summary:	Python 3 tools to manipulate font files
Summary(pl.UTF-8):	Narzędzia do manipulacji na plikach fontów dla Pythona 3
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4
%if "%{py3_ver}" < "3.7"
Requires:	python3-unicodedata2 >= 11.0.0
%endif

%description -n python3-fonttools
Python 3 tools to manipulate font files.

%description -n python3-fonttools -l pl.UTF-8
Narzędzia do manipulacji na plikach fontów dla Pythona 3.

%prep
%setup -q

%build
export LC_ALL=C.UTF-8
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=Lib \
%{__python} -m pytest Tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=Lib \
%{__python} -m pytest Tests
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/build-3/lib \
%{__make} -C Doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%py3_install
%endif

%if %{with python2}
%py_install

%py_postclean
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE LICENSE.external NEWS.rst README.rst
%attr(755,root,root) %{_bindir}/fonttools
%attr(755,root,root) %{_bindir}/pyftmerge
%attr(755,root,root) %{_bindir}/pyftsubset
%attr(755,root,root) %{_bindir}/ttx
%{_mandir}/man1/ttx.1*

%if %{with python2}
%files -n python-fonttools
%defattr(644,root,root,755)
%{py_sitescriptdir}/fontTools
%{py_sitescriptdir}/fonttools-%{version}-py*.egg-info

%if %{with doc}
%files -n python-fonttools-apidocs
%defattr(644,root,root,755)
%doc Doc/build/html/{_static,designspaceLib,misc,pens,ttLib,varLib,*.html,*.js}
%endif
%endif

%if %{with python3}
%files -n python3-fonttools
%defattr(644,root,root,755)
%{py3_sitescriptdir}/fontTools
%{py3_sitescriptdir}/fonttools-%{version}-py*.egg-info
%endif
