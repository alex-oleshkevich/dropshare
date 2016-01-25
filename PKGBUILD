pkgbase=dropshare
pkgname=${pkgbase}-git
pkgver=r1.3edf97b
pkgrel=1
pkgdesc="Simple file sharer to Dropbox"
arch=('any')
license=('MIT')
url='https://github.com/alex-oleshkevich/dropshare'
makedepends=('git' 'python3' 'python-dropbox' 'xclip' 'python-notify2' 'python-pyqt5')
provides=("${pkgname}-git")
conflicts=("${pkgname}-git")
install=

source=(
    "${pkgname}"::"git+https://github.com/alex-oleshkevich/$pkgbase.git"
)
md5sums=(
    'SKIP'

)

pkgver() {
  cd "$pkgname"
  (
    set -o pipefail
    git describe --long --tag | sed -r 's/([^-]*-g)/r\1/;s/-/./g' ||
    printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
  )
}

prepare() {
    kdeprefix=$(kde4-config --localprefix)
}

package() {
    cd "$pkgname"
	install -D -m555 ${srcdir}/${pkgname}/dropshare.py ${pkgdir}/usr/bin/dropshare
	install -D -m644 ${srcdir}/${pkgname}/dropshare.desktop ${pkgdir}/usr/share/applications/${pkgname}.desktop
	install -D -m644 ${srcdir}/${pkgname}/dolphin-action.desktop ${pkgdir}/usr/share/kde4/services/ServiceMenus/dropshare.desktop
	install -D -m644 ${srcdir}/${pkgname}/icon.svg ${pkgdir}/usr/share/icons/hicolor/16x16/apps/dropshare.svg
	install -D -m644 ${srcdir}/${pkgname}/icon.svg ${pkgdir}/usr/share/icons/hicolor/32x32/apps/dropshare.svg
	install -D -m644 ${srcdir}/${pkgname}/icon.svg ${pkgdir}/usr/share/icons/hicolor/48x48/apps/dropshare.svg
	install -D -m644 ${srcdir}/${pkgname}/icon.svg ${pkgdir}/usr/share/icons/hicolor/64x64/apps/dropshare.svg
	install -D -m644 ${srcdir}/${pkgname}/icon.svg ${pkgdir}/usr/share/icons/hicolor/128x128/apps/dropshare.svg
	install -D -m644 ${srcdir}/${pkgname}/authwindow.ui ${pkgdir}/usr/share/dropshare/authwindow.ui
}

