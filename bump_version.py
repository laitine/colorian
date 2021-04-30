import xml.etree.ElementTree


def main():

    bumped_version = input('Set release version (x.x.x): ')

    try:
        bundle_plist = xml.etree.ElementTree.parse(
            'dist/Colorian.app/Contents/Info.plist')

        is_next = False
        for idx, node in enumerate(bundle_plist.find('dict')):
            if is_next:
                node.text = bumped_version
                break
            if node.text == 'CFBundleShortVersionString':
                is_next = True

        bundle_plist.write('dist/Colorian.app/Contents/Info.plist')

    except OSError:
        print('Failed bumping Mac OSX application version!')
        return


if __name__ == '__main__':
    main()
