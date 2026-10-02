# Linux 固定 CI 构建参考

2026-09-30 从 `.github/workflows/flutter-build.yml` 提取。执行使用冻结提交中的完整工作流，不能把以下 job 单独粘贴为另一条生产路线。工具链：Rust 1.75、Flutter 3.24.5、LLVM 15.0.6、vcpkg 基线 `120deac3062162151622ca4860575a33844ba10b`。Focused profile 仅 Linux x86_64；入口 `.github/workflows/kemi-distribution.yml`。

```yaml
  build-rustdesk-linux:
    needs: [generate-bridge]
    name: build rustdesk linux ${{ matrix.job.target }}
    runs-on: ${{ matrix.job.on }}
    timeout-minutes: 90
    strategy:
      fail-fast: false
      matrix:
        job: ${{ fromJSON(inputs.build-profile == 'kemi-distribution' && '[{"arch":"x86_64","target":"x86_64-unknown-linux-gnu","distro":"ubuntu18.04","on":"ubuntu-22.04","deb_arch":"amd64","vcpkg-triplet":"x64-linux"}]' || '[{"arch":"x86_64","target":"x86_64-unknown-linux-gnu","distro":"ubuntu18.04","on":"ubuntu-22.04","deb_arch":"amd64","vcpkg-triplet":"x64-linux"},{"arch":"aarch64","target":"aarch64-unknown-linux-gnu","distro":"ubuntu18.04","on":"ubuntu-22.04-arm","deb_arch":"arm64","vcpkg-triplet":"arm64-linux"}]') }}
    steps:
      - name: Export GitHub Actions cache environment variables
        uses: actions/github-script@d7906e4ad0b1822421a7e6a35d5ca353c962f410 # v6
        with:
          script: |
            core.exportVariable('ACTIONS_CACHE_URL', process.env.ACTIONS_CACHE_URL || '');
            core.exportVariable('ACTIONS_RUNTIME_TOKEN', process.env.ACTIONS_RUNTIME_TOKEN || '');

      - name: Maximize build space
        run: |
          sudo rm -rf /opt/ghc
          sudo rm -rf /usr/local/lib/android
          sudo rm -rf /usr/share/dotnet
          sudo apt-get update -y
          sudo apt-get install -y nasm
          if [[ "${{ matrix.job.arch }}" == "x86_64" ]]; then
            sudo apt-get install -y qemu-user-static
          fi

      - name: Checkout source code
        uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4
        with:
          submodules: recursive

      - name: Apply KEMI server defaults
        if: ${{ inputs.build-profile == 'kemi-distribution' }}
        shell: bash
        run: |
          git -C libs/hbb_common apply --unidiff-zero "$GITHUB_WORKSPACE/.github/patches/kemi_hbb_common_server.diff"
          git -C libs/hbb_common apply --unidiff-zero "$GITHUB_WORKSPACE/.github/patches/kemi_hbb_common_android_rdv_status.diff"

      - name: Set Swap Space
        if: ${{ matrix.job.arch == 'x86_64' }}
        uses: pierotofy/set-swap-space@49819abfb41bd9b44fb781159c033dba90353a7c # v1.0
        with:
          swap-size-gb: 12

      - name: Free Space
        run: |
          df -h
          free -m

      - name: Install Rust toolchain
        uses: dtolnay/rust-toolchain@e97e2d8cc328f1b50210efc529dca0028893a2d9 # v1
        if: matrix.job.arch == 'x86_64' || env.UPLOAD_ARTIFACT == 'true'
        with:
          toolchain: ${{ env.RUST_VERSION }}
          targets: ${{ matrix.job.target }}
          components: "rustfmt"

      - name: Save Rust toolchain version
        run: |
          RUST_TOOLCHAIN_VERSION=$(cargo --version | awk '{print $2}')
          echo "RUST_TOOLCHAIN_VERSION=$RUST_TOOLCHAIN_VERSION" >> $GITHUB_ENV

      - name: Disable rust bridge build
        run: |
          # only build cdylib
          sed -i  "s/\[\"cdylib\", \"staticlib\", \"rlib\"\]/\[\"cdylib\"\]/g" Cargo.toml

      - name: Restore bridge files
        if: matrix.job.arch == 'x86_64' || env.UPLOAD_ARTIFACT == 'true'
        uses: actions/download-artifact@3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c # v8.0.1
        with:
          name: bridge-artifact
          path: ./

      - name: Setup vcpkg with Github Actions binary cache
        if: matrix.job.arch == 'x86_64' || env.UPLOAD_ARTIFACT == 'true'
        uses: lukka/run-vcpkg@b1a0dd252f06b9e25b3c022a9a03bd7a427fb6a2 # v11
        with:
          vcpkgDirectory: /opt/artifacts/vcpkg
          vcpkgGitCommitId: ${{ env.VCPKG_COMMIT_ID }}
          doNotCache: false

      - name: Install vcpkg dependencies
        if: matrix.job.arch == 'x86_64' || env.UPLOAD_ARTIFACT == 'true'
        run: |
          sudo apt install -y libva-dev && apt show libva-dev
          if ! $VCPKG_ROOT/vcpkg \
            install \
            --triplet ${{ matrix.job.vcpkg-triplet }} \
            --x-install-root="$VCPKG_ROOT/installed"; then
            find "${VCPKG_ROOT}/" -name "*.log" | while read -r _1; do
              echo "$_1:"
              echo "======"
              cat "$_1"
              echo "======"
              echo ""
            done
            exit 1
          fi
          head -n 100 "${VCPKG_ROOT}/buildtrees/ffmpeg/build-${{ matrix.job.vcpkg-triplet }}-rel-out.log" || true
        shell: bash

      - name: Restore bridge files
        if: matrix.job.arch == 'x86_64' || env.UPLOAD_ARTIFACT == 'true'
        uses: actions/download-artifact@3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c # v8.0.1
        with:
          name: bridge-artifact
          path: ./

      - uses: rustdesk-org/run-on-arch-action@d3fcfbb632b84cf7f6bc772bfaaa2c2f4f8789a8 # no release tag; commit 2026-05-26
        name: Build rustdesk
        id: vcpkg
        if: matrix.job.arch == 'x86_64' || env.UPLOAD_ARTIFACT == 'true'
        with:
          arch: ${{ matrix.job.arch }}
          distro: ${{ matrix.job.distro }}
          githubToken: ${{ github.token }}
          setup: |
            ls -l "${PWD}"
            ls -l /opt/artifacts/vcpkg/installed
          dockerRunArgs: |
            --volume "${PWD}:/workspace"
            --volume "/opt/artifacts:/opt/artifacts"
          shell: /bin/bash
          install: |
            apt-get update -y
            echo -e "installing deps"
            apt-get install -y \
               build-essential \
               clang \
               cmake \
               curl \
               gcc \
               git \
               g++ \
               libayatana-appindicator3-dev \
               libasound2-dev \
               libclang-10-dev \
               libgstreamer1.0-dev \
               libgstreamer-plugins-base1.0-dev \
               libgtk-3-dev \
               libpam0g-dev \
               libpulse-dev \
               libva-dev \
               libxcb-randr0-dev \
               libxcb-shape0-dev \
               libxcb-xfixes0-dev \
               libxdo-dev \
               libxfixes-dev \
               llvm-10-dev \
               nasm \
               ninja-build \
               pkg-config \
               tree \
               python3 \
               rpm \
               unzip \
               wget \
               xz-utils \
               libssl-dev
            # we have libopus compiled by us.
            apt-get remove -y libopus-dev || true
            # output devs
            ls -l ./
            tree -L 3 /opt/artifacts/vcpkg/installed
          run: |
            # disable git safe.directory
            git config --global --add safe.directory "*"
            # rust
            pushd /opt
            # do not use rustup, because memory overflow in qemu
            wget -O rust.tar.gz https://static.rust-lang.org/dist/rust-${{env.RUST_TOOLCHAIN_VERSION}}-${{ matrix.job.target }}.tar.gz
            tar -zxvf rust.tar.gz > /dev/null && rm rust.tar.gz
            cd rust-${{env.RUST_TOOLCHAIN_VERSION}}-${{ matrix.job.target }} && ./install.sh
            rm -rf rust-${{env.RUST_TOOLCHAIN_VERSION}}-${{ matrix.job.target }}
            # edit config
            mkdir -p ~/.cargo/
            echo """
              [source.crates-io]
              registry = 'https://github.com/rust-lang/crates.io-index'
            """ > ~/.cargo/config
            cat ~/.cargo/config
            # start build
            pushd /workspace
            export VCPKG_ROOT=/opt/artifacts/vcpkg
            if [[ "${{ matrix.job.arch }}" == "aarch64" ]]; then
              export JOBS="--jobs 3"
            else
              export JOBS=""
            fi
            echo $JOBS
            cargo build --locked --lib $JOBS --features hwcodec,flutter,unix-file-copy-paste --release
            rm -rf target/release/deps target/release/build
            rm -rf ~/.cargo

            # Setup Flutter
            # disable git safe.directory
            git config --global --add safe.directory "*"
            pushd /workspace
            case ${{ matrix.job.arch }} in
              aarch64)
                export PATH=/opt/flutter-elinux/bin:$PATH
                sed -i "s/flutter build linux --release/flutter-elinux build linux --verbose/g" ./build.py
                sed -i "s/x64\/release/arm64\/release/g" ./build.py
              ;;
              x86_64)
                export PATH=/opt/flutter/bin:$PATH
              ;;
            esac
            popd
            pushd /opt
            wget https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_${{ env.FLUTTER_VERSION }}-stable.tar.xz
            tar xf flutter_linux_${{ env.FLUTTER_VERSION }}-stable.tar.xz
            case ${{ matrix.job.arch }} in
              aarch64)
                # clone repo and reset to flutter ${{ env.FLUTTER_VERSION }}
                git clone https://github.com/sony/flutter-elinux.git || true
                pushd flutter-elinux
                  git fetch
                  git reset --hard ${{ env.FLUTTER_VERSION }}
                  bin/flutter-elinux doctor -v
                  bin/flutter-elinux precache --linux
                popd
                cp -R flutter/bin/cache/artifacts/engine/linux-x64/shader_lib flutter-elinux/flutter/bin/cache/artifacts/engine/linux-arm64
                rm -rf flutter
              ;;
              x86_64)
                flutter doctor -v
              ;;
            esac

            if [[ "3.24.5" == ${{ env.FLUTTER_VERSION }} ]]; then
              case ${{ matrix.job.arch }} in
                aarch64)
                  pushd /opt/flutter-elinux/flutter
                ;;
                x86_64)
                  pushd /opt/flutter
                ;;
              esac
              git apply ${{ github.workspace }}/.github/patches/flutter_3.24.4_dropdown_menu_enableFilter.diff
              popd
            fi

            # build flutter
            pushd /workspace
            export CARGO_INCREMENTAL=0
            export DEB_ARCH=${{ matrix.job.deb_arch }}
            python3 ./build.py --flutter --skip-cargo
            for name in rustdesk*??.deb; do
              mv "$name" "${name%%.deb}-${{ matrix.job.arch }}.deb"
            done

            # rpm package
            echo -e "start packaging fedora package"
            pushd /workspace
            case ${{ matrix.job.arch }} in
              aarch64)
                sed -i "s/linux\/x64/linux\/arm64/g" ./res/rpm-flutter.spec
                ;;
            esac
            HBB=`pwd` rpmbuild ./res/rpm-flutter.spec -bb
            pushd ~/rpmbuild/RPMS/${{ matrix.job.arch }}
            for name in rustdesk*??.rpm; do
                mv "$name" /workspace/"${name%%.rpm}.rpm"
            done

            # rpm suse package
            echo -e "start packaging suse package"
            pushd /workspace
            case ${{ matrix.job.arch }} in
              aarch64)
                sed -i "s/linux\/x64/linux\/arm64/g" ./res/rpm-flutter-suse.spec
                ;;
            esac
            HBB=`pwd` rpmbuild ./res/rpm-flutter-suse.spec -bb
            pushd ~/rpmbuild/RPMS/${{ matrix.job.arch }}
            for name in rustdesk*??.rpm; do
                mv "$name" /workspace/"${name%%.rpm}-suse.rpm"
            done

      - name: Publish debian/rpm package
        if: env.UPLOAD_ARTIFACT == 'true' && inputs.publish-release
        uses: softprops/action-gh-release@de2c0eb89ae2a093876385947365aca7b0e5f844 # v1
        with:
          prerelease: true
          tag_name: ${{ env.TAG_NAME }}
          files: |
            rustdesk-*.deb
            rustdesk-*.rpm

      - name: Upload deb
        uses: actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a # v7.0.1
        if: env.UPLOAD_ARTIFACT == 'true'
        with:
          name: rustdesk-${{ env.VERSION }}-${{ matrix.job.arch }}.deb
          path: rustdesk-${{ env.VERSION }}-${{ matrix.job.arch }}.deb

      # only x86_64 for arch since we can not find newest arm64 docker image to build
      # old arch image does not make sense for arch since it is "arch" which always update to date
      # and failed to makepkg arm64 on x86_64
      - name: Patch archlinux PKGBUILD
        if: matrix.job.arch == 'x86_64' && env.UPLOAD_ARTIFACT == 'true'
        run: |
          sed -i "s/x86_64/${{ matrix.job.arch }}/g" res/PKGBUILD
          if [[ "${{ matrix.job.arch }}" == "aarch64" ]]; then
            sed -i "s/x86_64/aarch64/g" ./res/PKGBUILD
          fi

      - name: Build archlinux package
        if: matrix.job.arch == 'x86_64' && env.UPLOAD_ARTIFACT == 'true'
        uses: rustdesk-org/arch-makepkg-action@04200739ed1d0bf6f2188b6736b26a767c57a7f9 # no release tag; commit 2026-05-26
        with:
          packages:
          scripts: |
            cd res && HBB=`pwd`/.. FLUTTER=1 makepkg -f

      - name: Publish archlinux package
        if: matrix.job.arch == 'x86_64' && env.UPLOAD_ARTIFACT == 'true' && inputs.publish-release
        uses: softprops/action-gh-release@de2c0eb89ae2a093876385947365aca7b0e5f844 # v1
        with:
          prerelease: true
          tag_name: ${{ env.TAG_NAME }}
          files: |
            res/rustdesk-${{ env.VERSION }}*.zst

  build-appimage:
    name: Build appimage ${{ matrix.job.target }}
    needs: [build-rustdesk-linux]
    runs-on: ubuntu-22.04
    if: ${{ inputs.upload-artifact }}
    timeout-minutes: 30
    strategy:
      fail-fast: false
      matrix:
        job: ${{ fromJSON(inputs.build-profile == 'kemi-distribution' && '[{"target":"x86_64-unknown-linux-gnu","arch":"x86_64"}]' || '[{"target":"x86_64-unknown-linux-gnu","arch":"x86_64"},{"target":"aarch64-unknown-linux-gnu","arch":"aarch64"}]') }}
    steps:
      - name: Checkout source code
        uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4
        with:
          submodules: recursive

      - name: Download Binary
        uses: actions/download-artifact@3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c # v8.0.1
        with:
          name: rustdesk-${{ env.VERSION }}-${{ matrix.job.arch }}.deb
          path: .

      - name: Rename Binary
        run: |
          mv rustdesk-${{ env.VERSION }}-${{ matrix.job.arch }}.deb appimage/rustdesk.deb

      - name: Build appimage package
        shell: bash
        run: |
          # install libarchive-tools for bsdtar command used in AppImageBuilder.yml
          sudo apt-get update -y
          # https://github.com/AppImage/AppImageKit/wiki/FUSE
          sudo apt-get install -y libarchive-tools libfuse2
          # set-up appimage-builder
          # https://github.com/AppImage/AppImageKit/issues/1395
          sudo pip3 install "setuptools_scm<10"
          sudo pip3 install git+https://github.com/rustdesk-org/appimage-builder.git
          # run appimage-builder
          pushd appimage
          sed -i "s/^    version: .*/    version: ${{ env.VERSION }}/" \
            ./AppImageBuilder-${{ matrix.job.arch }}.yml
          sudo appimage-builder --skip-tests --recipe ./AppImageBuilder-${{ matrix.job.arch }}.yml
          appimage_file="$(find . -maxdepth 1 -type f -name '*.AppImage' -print -quit)"
          output_file="rustdesk-${{ env.VERSION }}-${{ matrix.job.arch }}.AppImage"
          if [[ -n "$appimage_file" ]]; then
            if [[ "$(basename "$appimage_file")" != "$output_file" ]]; then
              mv "$appimage_file" "$output_file"
            fi
          else
            test -s AppDir.squashfs
            curl --fail --location --retry 5 --retry-all-errors \
              --output appimage-runtime \
              "https://github.com/AppImage/type2-runtime/releases/download/continuous/runtime-${{ matrix.job.arch }}"
            cat appimage-runtime AppDir.squashfs > "$output_file"
          fi
          sudo chmod +x "$output_file"
          test -s "$output_file"

      - name: Upload final Linux AppImage
        uses: actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a # v7.0.1
        with:
          name: kemi-linux-${{ matrix.job.arch }}-${{ github.sha }}
          path: ./appimage/rustdesk-${{ env.VERSION }}-*.AppImage
          retention-days: 14

      - name: Publish appimage package
        if: env.UPLOAD_ARTIFACT == 'true' && inputs.publish-release
        uses: softprops/action-gh-release@de2c0eb89ae2a093876385947365aca7b0e5f844 # v1
        with:
          prerelease: true
          tag_name: ${{ env.TAG_NAME }}
          files: |
            ./appimage/rustdesk-${{ env.VERSION }}-*.AppImage

```
