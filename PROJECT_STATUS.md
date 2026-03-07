# BSEYE 키오스크 모니터링 시스템 - 프로젝트 현황

**작성일**: 2026-03-07


## 1. 프로젝트 파일 구조

- **kiosk-monitor/**
  - .gitignore
  - D:BSEYEdistbseye_agent.exe
  - SERVER_SETUP_LOG.md
  - app.py
  - backup_db.sh
  - config.py
  - daily_snapshot.py
  - gunicorn.ctl
  - init_db.py
  - init_layout_db.py
  - pyinstaller
  - **.git/**
    - COMMIT_EDITMSG
    - HEAD
    - config
    - description
    - index
    - packed-refs
    - **branches/**
    - **hooks/**
      - applypatch-msg.sample
      - commit-msg.sample
      - fsmonitor-watchman.sample
      - post-update.sample
      - pre-applypatch.sample
      - pre-commit.sample
      - pre-merge-commit.sample
      - pre-push.sample
      - pre-rebase.sample
      - pre-receive.sample
      - prepare-commit-msg.sample
      - push-to-checkout.sample
      - update.sample
    - **info/**
      - exclude
    - **logs/**
      - HEAD
      - **refs/**
        - **heads/**
          - main
        - **remotes/**
          - **origin/**
            - main
    - **objects/**
      - **01/**
        - 25a2bb3d12fb529b48914229be0fb16a94cf51
      - **03/**
        - a812312d939aa85072da560039f0ed97b276ec
      - **05/**
        - 0e6040278832db2f0c40cd4e67a052a755d4cc
      - **08/**
        - 78bf4df06040f990f3c0a08a3424bc0059e435
      - **0b/**
        - a0d4bca72bbd46d79de780766a0599e6004434
      - **0f/**
        - 05d0903063c2ed94405ffb9267716ae622f635
        - 6eb58ae40c5ec8075638dbe768acc4d717137f
      - **10/**
        - 648cabcc4988ec29dc33868f28f2a7693065ed
      - **17/**
        - 0b2858508324ca43bbb5602dc9178d49c0d80a
      - **1b/**
        - c466b5634a7ddcc404476a16d3c289044517bc
      - **1d/**
        - 13e3ad465e535c5c5cde5394a5b346d4a58568
      - **1f/**
        - 414b287cb8e2e9b2c9135f17595eea7575c970
      - **20/**
        - 74798bf2227147542e4d388750720ff30b1df5
        - 7633c4975ec4283f7911353082761e33ed7496
      - **23/**
        - efbc91795dccff3b3116f4bb03741dda05203c
      - **25/**
        - 0f7fb89a06c5667047a5b98df19bcd850aacdd
      - **26/**
        - f7ad28e3ece4a1e397d98aa060e12d4c2fa3ae
      - **27/**
        - abc4a60976db05304fb2131317d0494b76a369
      - **2d/**
        - 370c3f4dcbeca80f596e6d295e7ccaedca0b95
        - 676fdbc38dcd4bf94ff79b2383454d407ace0d
      - **2f/**
        - 52c4b4a6a3fc367b5b1884b3c8b0a04bcb7bcb
      - **30/**
        - 554885b254d87a3a77b713991cf28e164d5eb0
      - **31/**
        - 997064d329dd00c5284a2c8da54b26c845c6ce
      - **33/**
        - c9e54949cbd778ab73d7da3f0ac590b4c38f93
      - **34/**
        - bdb244cc6eefef301eb6b39d9632511be7feae
      - **35/**
        - 211a3132353848d9064f0f9c998ab1de4f10cb
      - **37/**
        - 614bd47d6ecbbae8e80c23a24f8bd6a10b174f
      - **40/**
        - d882e657f02a2dafa9f97bbc6991bf84cf43ff
      - **47/**
        - 38f7116b54ebfa5b1f5d10fe5772eb162b825b
      - **4b/**
        - fed54d6c6c96b13d2de0cf842202c8dc3a90bb
      - **4c/**
        - d35dc07599b1c993b5009138acd6c36106b91d
      - **4e/**
        - 0ee39610498506c6b98a13b115cb8a6982c95e
        - 96dd6bb7164ee0aacfe6334d8cee51c954cd0d
      - **50/**
        - d2cabd71d916844ae2b242faebdcab5d0a535a
      - **51/**
        - 02431c0f5d17fd15d5de29c99e50bbec22e641
      - **53/**
        - 2df72aaee10424faf6d33d532f54118a6ec7c3
        - a69847b389ad186be343cebf0a3a2873b4f5d2
      - **54/**
        - 3f1837f1dd9e2a2e90792ee744ee4f99c192d8
        - 8dc57b3a364b870ffb7e67438fc5e178a5cd78
      - **55/**
        - 3eb186f3ffc770a1f228e0796237dc39b29004
      - **56/**
        - dcf5bb445d6b2f43f9df9f80e6c669719234e9
      - **58/**
        - 56ac67a3bb64c27c9680befaa6ec0f6e9b6206
        - aab43fe50d8bceab887e3241273bda9647c748
      - **5c/**
        - 972938f57b0d10fdf4d24a397b2c2c5877babd
        - b4f745ffc14985bf232f3190066330abc1cafb
      - **5e/**
        - 55570f9d59bf23b5161d3a7913b06da3c50e9a
      - **64/**
        - f08e0611553084bbc6c77f73d0bb1959710eed
      - **66/**
        - cc44a6be8b93fabd8d8a1e6828403e11419534
      - **68/**
        - 43fad3e48a94377fdebd1bf8bf65d1214543c3
        - ba9fc53ba28c9f0a871bb71e0a3bfb1edc853e
      - **6a/**
        - 50af74eaa738dc8fcbc0398035f1d21fb53f74
      - **6b/**
        - 253573c0c7532f5114982fe732e54dca310d25
      - **6e/**
        - 461aea63146daf167ddc9483d942a1b878495d
        - 7b6c1995e6c0d527b49a245e753f91030b8d31
      - **6f/**
        - b2f5e70ca4fcc4df6a0f881cc5ceccb1ea8cc3
      - **71/**
        - 00a534f31ba34f59a16b338c531699b5e082e4
      - **73/**
        - 5cc455a691f04f364f155bc1a35279b9a40053
      - **76/**
        - 9589ca2dcf34a591c9f8f6b7967a31d5819ca5
      - **77/**
        - 8afece4098135c8250fee8d2ee7340e5ea4515
      - **7e/**
        - 5a6f3f4d943132752f0ca34b8094ba72a7d3ed
      - **81/**
        - d9e469982f1675623107959113e6ae604033cd
      - **83/**
        - cb25354ab2160778d67e5c01c702e7afdb9f41
        - ceccf72b9e0fb814c6c3ad50875280284cf1f5
      - **87/**
        - 950ec26ae4f8caf40c08423fd70e90257302ed
        - ee538aaa26964734ae21a74ece0d8f7c4950da
      - **89/**
        - a5494df0dbfeaec52542d802a484a6cdb67ac4
      - **8a/**
        - 385268415f3e6ab7411088417ec44874873a9b
      - **8b/**
        - 885073050059688ebaad60414cd01398fab213
      - **8d/**
        - 9ef57172635a579f28790590f54ad2f072ff4b
      - **8e/**
        - ccd2914bc45b13d7d901b4b7a1f4edec274a07
      - **91/**
        - e9978cd3c2d0b4d114deaafe8850725a82a15b
      - **92/**
        - 2bc99dcb49b0a06e9aacba144079edf824aec8
      - **97/**
        - e60b8b16b7bb7b3658479edf577e527f71326f
      - **9c/**
        - 834c5e29ceb5c18549d475af3840f189bc8f01
      - **a3/**
        - e1f01b6d0b7a2a32a903ac3273fbe5b29dfe6c
      - **a5/**
        - 3c4e934f8d111609ccbced9ad12b28dfffed3d
        - 81a3ead133fb30263a46698b3d2e897b1fb4e9
      - **a6/**
        - b8f3082e5c81a66c5e66488559b2c4c4b50204
      - **a7/**
        - da86a0e9d6acb6e284e4418013755716d87d59
      - **af/**
        - 2228b4dc99a9a45c8e7a1e73e5693b8fef2a9d
      - **b2/**
        - 8e618cad3d671027ba83dad6a9095742513503
      - **b3/**
        - e6222a1050f4239b6fac20d376f27b2adb0c52
      - **b4/**
        - b8fbf9fa0b9d9cd282f92740cf99000363b3d2
      - **b8/**
        - 13defba537d4c1066faa3c1d3051c1f17f0de0
      - **bc/**
        - 26c2dabca15a859e8cf35847a6355834e1ed75
      - **bd/**
        - 5c4288c00825218d610ed64c64f64abce61017
      - **c0/**
        - 3a8083581f88cabc9678c1ccd66aceffe82b91
      - **c1/**
        - f1aa5067fdb8288b8e0fe14b0981cf0519a753
      - **c2/**
        - 2c2ba40f3776fb220becdd4e3a2aad37f5a3a2
      - **c5/**
        - 74313f95e977d04274a32f7d7a86d7e9858539
      - **c6/**
        - 68de2a66a3c3d36db95daf5d6296eea06fdc52
      - **c8/**
        - 0c843ed621e5496b672495c9feaceedf4a1ddf
      - **c9/**
        - aafff623f8f577f05e7410119cc9da8e9c537c
      - **ca/**
        - 1d77ecb0959d22aad21da36c17a73e4bcfe486
        - 36be45d86e3ae36d61b31cd60e4f36fddbcc46
      - **cc/**
        - f4dcd0a2a874e82f42f44ab92b9f3e8eb5bcca
      - **ce/**
        - 7bded332168b1960555b449903711809224001
      - **cf/**
        - 604d29412081f11e5b3afa010395afdaec089b
        - 8c91d8bb51bc5659715a12d1cb1de8fc2e5e7c
      - **d0/**
        - 3fa7de32c8f0c9954aa1ff0495bb36b2f26ddd
      - **d2/**
        - 9c26aa7a5f6cea2c925ff48799e0adaff6f0c0
      - **d4/**
        - 41770b937b51bfd54aae60c6205b7711ba0808
      - **d6/**
        - cda0da0a66eee98aa14c30f782bddfc7395ecb
      - **da/**
        - 8d17737015b25c48fed80fc571e1ef2142b18a
      - **dc/**
        - 81aab390059627762472abc1a3fcdbae9d8325
      - **df/**
        - a4615cd15fe41fe6efa8a210784991081534dd
      - **e1/**
        - 6a22d8a7db897759d0e6309daf9d619e5600b2
      - **e3/**
        - 0b406f671d048ffe7af6ac9a8cbdef79c423db
        - 7a6ab5710af4ce0954f7348f5bc1dac236399e
      - **e4/**
        - 455acbd480eb29c760237728a7dbca70219d91
      - **e5/**
        - a6c5a0bd37cf107be3122150b7a6aacaf64302
      - **e6/**
        - 9de29bb2d1d6434b8b29ae775ad8c2e48c5391
      - **e7/**
        - 3088cd2bc33f4d6a0369f6659fe648f172fd8e
      - **ec/**
        - 036aa8c67ccdb7af81cb3fd8d3babecd4d28d7
      - **ed/**
        - b67c2ce5eaf5eb0e26cc57ce151b298710ad8d
      - **f4/**
        - e2b1736cbf4039685106f4399c85d52ca230ab
      - **f5/**
        - 05646cdbda9d7e82dd528ffbac04f50dea9b19
      - **f7/**
        - bf4fff566b04c5bb7592833bd655e763965590
      - **fb/**
        - e593b465adf900ff9f9986834251c0ed7ca6ff
      - **fc/**
        - 85be5be03873923891e38d39f01534bb616acb
      - **fd/**
        - 3d19189ca98aa1bd7828ca15ac64bc662461ce
        - 3e388d96b757c67ecf7d9147eed0b79621a72d
      - **info/**
      - **pack/**
    - **refs/**
      - **heads/**
        - main
      - **remotes/**
        - **origin/**
          - main
      - **tags/**
  - **__pycache__/**
  - **agent/**
    - INSTALL_GUIDE.md
    - bseye_agent.py
  - **backup/**
  - **models/**
  - **routes/**
  - **services/**
  - **static/**
    - **agent/**
      - bseye-agent.zip
      - data_sender.py
      - db_manager.py
      - device_checker.py
      - hook_monitor.py
      - main.py
      - web_server.py
      - **templates/**
        - dashboard.html
    - **css/**
    - **js/**
  - **templates/**
    - admin_login_log.html
    - admin_user_form.html
    - admin_users.html
    - alarms.html
    - change_password.html
    - dashboard_preview.html
    - editor.html
    - executive.html
    - hospital_detail.html
    - hospital_view.html
    - hospitals.html
    - index.html
    - index_old.html
    - isv_detail.html
    - kiosk_editor.html
    - kiosk_preview.html
    - login.html
    - maintenance.html
    - monitoring.html
    - monitoring3.html
    - nav.html
    - setup_monitor.html
    - ticket_detail.html
    - ticket_form.html
    - tickets.html
    - usage.html
    - usage_verify.html
  - **venv/**
    - pyvenv.cfg
    - **bin/**
      - Activate.ps1
      - activate
      - activate.csh
      - activate.fish
      - flask
      - gunicorn
      - gunicornc
      - pip
      - pip3
      - pip3.10
      - pyi-archive_viewer
      - pyi-bindepend
      - pyi-grab_version
      - pyi-makespec
      - pyi-set_version
      - pyinstaller
      - python
      - python3
      - python3.10
    - **include/**
      - **site/**
        - **python3.10/**
          - **greenlet/**
            - greenlet.h
    - **lib/**
      - **python3.10/**
        - **site-packages/**
          - distutils-precedence.pth
          - pyodbc.cpython-310-x86_64-linux-gnu.so
          - pyodbc.pyi
          - **Flask_JWT_Extended-4.7.1.dist-info/**
            - INSTALLER
            - LICENSE
            - METADATA
            - RECORD
            - REQUESTED
            - WHEEL
            - top_level.txt
          - **Flask_Login-0.6.3.dist-info/**
            - INSTALLER
            - LICENSE
            - METADATA
            - RECORD
            - REQUESTED
            - WHEEL
            - top_level.txt
          - **PyInstaller/**
            - __init__.py
            - __main__.py
            - _recursion_too_deep_message.py
            - _shared_with_waf.py
            - compat.py
            - config.py
            - configure.py
            - exceptions.py
            - log.py
            - **__pycache__/**
            - **archive/**
              - __init__.py
              - pyz_crypto.py
              - readers.py
              - writers.py
              - **__pycache__/**
            - **bootloader/**
              - **Linux-64bit-intel/**
                - run
                - run_d
            - **building/**
              - __init__.py
              - api.py
              - build_main.py
              - datastruct.py
              - icon.py
              - makespec.py
              - osx.py
              - splash.py
              - splash_templates.py
              - templates.py
              - utils.py
              - **__pycache__/**
            - **depend/**
              - __init__.py
              - analysis.py
              - bindepend.py
              - bytecode.py
              - dylib.py
              - imphook.py
              - imphookapi.py
              - utils.py
              - **__pycache__/**
            - **fake-modules/**
              - pyi_splash.py
              - **__pycache__/**
              - **_pyi_rth_utils/**
                - __init__.py
                - _win32.py
                - qt.py
                - tempfile.py
                - **__pycache__/**
            - **hooks/**
              - __init__.py
              - hook-PIL.Image.py
              - hook-PIL.ImageFilter.py
              - hook-PIL.SpiderImagePlugin.py
              - hook-PIL.py
              - hook-PyQt5.QAxContainer.py
              - hook-PyQt5.Qsci.py
              - hook-PyQt5.Qt.py
              - hook-PyQt5.Qt3DAnimation.py
              - hook-PyQt5.Qt3DCore.py
              - hook-PyQt5.Qt3DExtras.py
              - hook-PyQt5.Qt3DInput.py
              - hook-PyQt5.Qt3DLogic.py
              - hook-PyQt5.Qt3DRender.py
              - hook-PyQt5.QtBluetooth.py
              - hook-PyQt5.QtChart.py
              - hook-PyQt5.QtCore.py
              - hook-PyQt5.QtDBus.py
              - hook-PyQt5.QtDataVisualization.py
              - hook-PyQt5.QtDesigner.py
              - hook-PyQt5.QtGui.py
              - hook-PyQt5.QtHelp.py
              - hook-PyQt5.QtLocation.py
              - hook-PyQt5.QtMacExtras.py
              - hook-PyQt5.QtMultimedia.py
              - hook-PyQt5.QtMultimediaWidgets.py
              - hook-PyQt5.QtNetwork.py
              - hook-PyQt5.QtNetworkAuth.py
              - hook-PyQt5.QtNfc.py
              - hook-PyQt5.QtOpenGL.py
              - hook-PyQt5.QtPositioning.py
              - hook-PyQt5.QtPrintSupport.py
              - hook-PyQt5.QtPurchasing.py
              - hook-PyQt5.QtQml.py
              - hook-PyQt5.QtQuick.py
              - hook-PyQt5.QtQuick3D.py
              - hook-PyQt5.QtQuickWidgets.py
              - hook-PyQt5.QtRemoteObjects.py
              - hook-PyQt5.QtScript.py
              - hook-PyQt5.QtSensors.py
              - hook-PyQt5.QtSerialPort.py
              - hook-PyQt5.QtSql.py
              - hook-PyQt5.QtSvg.py
              - hook-PyQt5.QtTest.py
              - hook-PyQt5.QtTextToSpeech.py
              - hook-PyQt5.QtWebChannel.py
              - hook-PyQt5.QtWebEngine.py
              - hook-PyQt5.QtWebEngineCore.py
              - hook-PyQt5.QtWebEngineWidgets.py
              - hook-PyQt5.QtWebKit.py
              - hook-PyQt5.QtWebKitWidgets.py
              - hook-PyQt5.QtWebSockets.py
              - hook-PyQt5.QtWidgets.py
              - hook-PyQt5.QtWinExtras.py
              - hook-PyQt5.QtX11Extras.py
              - hook-PyQt5.QtXml.py
              - hook-PyQt5.QtXmlPatterns.py
              - hook-PyQt5.py
              - hook-PyQt5.uic.py
              - hook-PyQt6.QAxContainer.py
              - hook-PyQt6.Qsci.py
              - hook-PyQt6.Qt3DAnimation.py
              - hook-PyQt6.Qt3DCore.py
              - hook-PyQt6.Qt3DExtras.py
              - hook-PyQt6.Qt3DInput.py
              - hook-PyQt6.Qt3DLogic.py
              - hook-PyQt6.Qt3DRender.py
              - hook-PyQt6.QtBluetooth.py
              - hook-PyQt6.QtCharts.py
              - hook-PyQt6.QtCore.py
              - hook-PyQt6.QtDBus.py
              - hook-PyQt6.QtDataVisualization.py
              - hook-PyQt6.QtDesigner.py
              - hook-PyQt6.QtGraphs.py
              - hook-PyQt6.QtGraphsWidgets.py
              - hook-PyQt6.QtGui.py
              - hook-PyQt6.QtHelp.py
              - hook-PyQt6.QtMultimedia.py
              - hook-PyQt6.QtMultimediaWidgets.py
              - hook-PyQt6.QtNetwork.py
              - hook-PyQt6.QtNetworkAuth.py
              - hook-PyQt6.QtNfc.py
              - hook-PyQt6.QtOpenGL.py
              - hook-PyQt6.QtOpenGLWidgets.py
              - hook-PyQt6.QtPdf.py
              - hook-PyQt6.QtPdfWidgets.py
              - hook-PyQt6.QtPositioning.py
              - hook-PyQt6.QtPrintSupport.py
              - hook-PyQt6.QtQml.py
              - hook-PyQt6.QtQuick.py
              - hook-PyQt6.QtQuick3D.py
              - hook-PyQt6.QtQuickWidgets.py
              - hook-PyQt6.QtRemoteObjects.py
              - hook-PyQt6.QtSensors.py
              - hook-PyQt6.QtSerialPort.py
              - hook-PyQt6.QtSpatialAudio.py
              - hook-PyQt6.QtSql.py
              - hook-PyQt6.QtStateMachine.py
              - hook-PyQt6.QtSvg.py
              - hook-PyQt6.QtSvgWidgets.py
              - hook-PyQt6.QtTest.py
              - hook-PyQt6.QtTextToSpeech.py
              - hook-PyQt6.QtWebChannel.py
              - hook-PyQt6.QtWebEngineCore.py
              - hook-PyQt6.QtWebEngineQuick.py
              - hook-PyQt6.QtWebEngineWidgets.py
              - hook-PyQt6.QtWebSockets.py
              - hook-PyQt6.QtWidgets.py
              - hook-PyQt6.QtXml.py
              - hook-PyQt6.py
              - hook-PyQt6.uic.py
              - hook-PySide2.Qt3DAnimation.py
              - hook-PySide2.Qt3DCore.py
              - hook-PySide2.Qt3DExtras.py
              - hook-PySide2.Qt3DInput.py
              - hook-PySide2.Qt3DLogic.py
              - hook-PySide2.Qt3DRender.py
              - hook-PySide2.QtAxContainer.py
              - hook-PySide2.QtCharts.py
              - hook-PySide2.QtConcurrent.py
              - hook-PySide2.QtCore.py
              - hook-PySide2.QtDataVisualization.py
              - hook-PySide2.QtGui.py
              - hook-PySide2.QtHelp.py
              - hook-PySide2.QtLocation.py
              - hook-PySide2.QtMacExtras.py
              - hook-PySide2.QtMultimedia.py
              - hook-PySide2.QtMultimediaWidgets.py
              - hook-PySide2.QtNetwork.py
              - hook-PySide2.QtOpenGL.py
              - hook-PySide2.QtOpenGLFunctions.py
              - hook-PySide2.QtPositioning.py
              - hook-PySide2.QtPrintSupport.py
              - hook-PySide2.QtQml.py
              - hook-PySide2.QtQuick.py
              - hook-PySide2.QtQuickControls2.py
              - hook-PySide2.QtQuickWidgets.py
              - hook-PySide2.QtRemoteObjects.py
              - hook-PySide2.QtScript.py
              - hook-PySide2.QtScriptTools.py
              - hook-PySide2.QtScxml.py
              - hook-PySide2.QtSensors.py
              - hook-PySide2.QtSerialPort.py
              - hook-PySide2.QtSql.py
              - hook-PySide2.QtSvg.py
              - hook-PySide2.QtTest.py
              - hook-PySide2.QtTextToSpeech.py
              - hook-PySide2.QtUiTools.py
              - hook-PySide2.QtWebChannel.py
              - hook-PySide2.QtWebEngine.py
              - hook-PySide2.QtWebEngineCore.py
              - hook-PySide2.QtWebEngineWidgets.py
              - hook-PySide2.QtWebKit.py
              - hook-PySide2.QtWebKitWidgets.py
              - hook-PySide2.QtWebSockets.py
              - hook-PySide2.QtWidgets.py
              - hook-PySide2.QtWinExtras.py
              - hook-PySide2.QtX11Extras.py
              - hook-PySide2.QtXml.py
              - hook-PySide2.QtXmlPatterns.py
              - hook-PySide2.Qwt5.py
              - hook-PySide2.py
              - hook-PySide6.Qt3DAnimation.py
              - hook-PySide6.Qt3DCore.py
              - hook-PySide6.Qt3DExtras.py
              - hook-PySide6.Qt3DInput.py
              - hook-PySide6.Qt3DLogic.py
              - hook-PySide6.Qt3DRender.py
              - hook-PySide6.QtAxContainer.py
              - hook-PySide6.QtBluetooth.py
              - hook-PySide6.QtCharts.py
              - hook-PySide6.QtConcurrent.py
              - hook-PySide6.QtCore.py
              - hook-PySide6.QtDBus.py
              - hook-PySide6.QtDataVisualization.py
              - hook-PySide6.QtDesigner.py
              - hook-PySide6.QtGraphs.py
              - hook-PySide6.QtGraphsWidgets.py
              - hook-PySide6.QtGui.py
              - hook-PySide6.QtHelp.py
              - hook-PySide6.QtHttpServer.py
              - hook-PySide6.QtLocation.py
              - hook-PySide6.QtMultimedia.py
              - hook-PySide6.QtMultimediaWidgets.py
              - hook-PySide6.QtNetwork.py
              - hook-PySide6.QtNetworkAuth.py
              - hook-PySide6.QtNfc.py
              - hook-PySide6.QtOpenGL.py
              - hook-PySide6.QtOpenGLWidgets.py
              - hook-PySide6.QtPdf.py
              - hook-PySide6.QtPdfWidgets.py
              - hook-PySide6.QtPositioning.py
              - hook-PySide6.QtPrintSupport.py
              - hook-PySide6.QtQml.py
              - hook-PySide6.QtQuick.py
              - hook-PySide6.QtQuick3D.py
              - hook-PySide6.QtQuickControls2.py
              - hook-PySide6.QtQuickWidgets.py
              - hook-PySide6.QtRemoteObjects.py
              - hook-PySide6.QtScxml.py
              - hook-PySide6.QtSensors.py
              - hook-PySide6.QtSerialBus.py
              - hook-PySide6.QtSerialPort.py
              - hook-PySide6.QtSpatialAudio.py
              - hook-PySide6.QtSql.py
              - hook-PySide6.QtStateMachine.py
              - hook-PySide6.QtSvg.py
              - hook-PySide6.QtSvgWidgets.py
              - hook-PySide6.QtTest.py
              - hook-PySide6.QtTextToSpeech.py
              - hook-PySide6.QtUiTools.py
              - hook-PySide6.QtWebChannel.py
              - hook-PySide6.QtWebEngineCore.py
              - hook-PySide6.QtWebEngineQuick.py
              - hook-PySide6.QtWebEngineWidgets.py
              - hook-PySide6.QtWebSockets.py
              - hook-PySide6.QtWidgets.py
              - hook-PySide6.QtXml.py
              - hook-PySide6.py
              - hook-_ctypes.py
              - hook-_osx_support.py
              - hook-_pyi_rth_utils.py
              - hook-_tkinter.py
              - hook-babel.py
              - hook-difflib.py
              - hook-distutils.command.check.py
              - hook-distutils.py
              - hook-distutils.util.py
              - hook-django.contrib.sessions.py
              - hook-django.core.cache.py
              - hook-django.core.mail.py
              - hook-django.core.management.py
              - hook-django.db.backends.mysql.base.py
              - hook-django.db.backends.oracle.base.py
              - hook-django.db.backends.py
              - hook-django.py
              - hook-django.template.loaders.py
              - hook-encodings.py
              - hook-gevent.py
              - hook-gi.py
              - hook-gi.repository.Adw.py
              - hook-gi.repository.AppIndicator3.py
              - hook-gi.repository.Atk.py
              - hook-gi.repository.AyatanaAppIndicator3.py
              - hook-gi.repository.Champlain.py
              - hook-gi.repository.Clutter.py
              - hook-gi.repository.DBus.py
              - hook-gi.repository.GIRepository.py
              - hook-gi.repository.GLib.py
              - hook-gi.repository.GModule.py
              - hook-gi.repository.GObject.py
              - hook-gi.repository.Gdk.py
              - hook-gi.repository.GdkPixbuf.py
              - hook-gi.repository.Gio.py
              - hook-gi.repository.Graphene.py
              - hook-gi.repository.Gsk.py
              - hook-gi.repository.Gst.py
              - hook-gi.repository.GstAllocators.py
              - hook-gi.repository.GstApp.py
              - hook-gi.repository.GstAudio.py
              - hook-gi.repository.GstBadAudio.py
              - hook-gi.repository.GstBase.py
              - hook-gi.repository.GstCheck.py
              - hook-gi.repository.GstCodecs.py
              - hook-gi.repository.GstController.py
              - hook-gi.repository.GstGL.py
              - hook-gi.repository.GstGLEGL.py
              - hook-gi.repository.GstGLWayland.py
              - hook-gi.repository.GstGLX11.py
              - hook-gi.repository.GstInsertBin.py
              - hook-gi.repository.GstMpegts.py
              - hook-gi.repository.GstNet.py
              - hook-gi.repository.GstPbutils.py
              - hook-gi.repository.GstPlay.py
              - hook-gi.repository.GstPlayer.py
              - hook-gi.repository.GstRtp.py
              - hook-gi.repository.GstRtsp.py
              - hook-gi.repository.GstRtspServer.py
              - hook-gi.repository.GstSdp.py
              - hook-gi.repository.GstTag.py
              - hook-gi.repository.GstTranscoder.py
              - hook-gi.repository.GstVideo.py
              - hook-gi.repository.GstVulkan.py
              - hook-gi.repository.GstVulkanWayland.py
              - hook-gi.repository.GstVulkanXCB.py
              - hook-gi.repository.GstWebRTC.py
              - hook-gi.repository.Gtk.py
              - hook-gi.repository.GtkChamplain.py
              - hook-gi.repository.GtkClutter.py
              - hook-gi.repository.GtkSource.py
              - hook-gi.repository.GtkosxApplication.py
              - hook-gi.repository.HarfBuzz.py
              - hook-gi.repository.OsmGpsMap.py
              - hook-gi.repository.Pango.py
              - hook-gi.repository.PangoCairo.py
              - hook-gi.repository.Rsvg.py
              - hook-gi.repository.cairo.py
              - hook-gi.repository.freetype2.py
              - hook-gi.repository.xlib.py
              - hook-heapq.py
              - hook-idlelib.py
              - hook-importlib_metadata.py
              - hook-importlib_resources.py
              - hook-keyring.py
              - hook-kivy.py
              - hook-lib2to3.py
              - hook-matplotlib.backend_bases.py
              - hook-matplotlib.backends.backend_qtagg.py
              - hook-matplotlib.backends.backend_qtcairo.py
              - hook-matplotlib.backends.py
              - hook-matplotlib.backends.qt_compat.py
              - hook-matplotlib.numerix.py
              - hook-matplotlib.py
              - hook-matplotlib.pyplot.py
              - hook-multiprocessing.util.py
              - hook-numpy.py
              - hook-pandas.io.clipboard.py
              - hook-pandas.io.formats.style.py
              - hook-pandas.plotting.py
              - hook-pandas.py
              - hook-pickle.py
              - hook-pkg_resources.py
              - hook-platform.py
              - hook-pygments.py
              - hook-pytz.py
              - hook-pytzdata.py
              - hook-qtawesome.py
              - hook-qtpy.py
              - hook-scapy.layers.all.py
              - hook-scipy.io.matlab.py
              - hook-scipy.linalg.py
              - hook-scipy.py
              - hook-scipy.sparse.csgraph.py
              - hook-scipy.spatial._ckdtree.py
              - hook-scipy.spatial.transform.rotation.py
              - hook-scipy.special._ellip_harm_2.py
              - hook-scipy.special._ufuncs.py
              - hook-scipy.stats._stats.py
              - hook-scrapy.py
              - hook-setuptools._vendor.importlib_metadata.py
              - hook-setuptools._vendor.jaraco.text.py
              - hook-setuptools.py
              - hook-shelve.py
              - hook-shiboken6.py
              - hook-sphinx.py
              - hook-sqlalchemy.py
              - hook-sqlite3.py
              - hook-sysconfig.py
              - hook-wcwidth.py
              - hook-win32ctypes.core.py
              - hook-xml.dom.domreg.py
              - hook-xml.etree.cElementTree.py
              - hook-xml.py
              - hook-zope.interface.py
              - rthooks.dat
              - **__pycache__/**
              - **pre_find_module_path/**
                - __init__.py
                - hook-PyQt5.uic.port_v2.py
                - hook-_pyi_rth_utils.py
                - hook-distutils.py
                - hook-pyi_splash.py
                - hook-tkinter.py
                - **__pycache__/**
              - **pre_safe_import_module/**
                - __init__.py
                - hook-autocommand.py
                - hook-backports.py
                - hook-backports.tarfile.py
                - hook-distutils.py
                - hook-gi.overrides.py
                - hook-gi.py
                - hook-gi.repository.Adw.py
                - hook-gi.repository.AppIndicator3.py
                - hook-gi.repository.Atk.py
                - hook-gi.repository.AyatanaAppIndicator3.py
                - hook-gi.repository.Champlain.py
                - hook-gi.repository.Clutter.py
                - hook-gi.repository.DBus.py
                - hook-gi.repository.GIRepository.py
                - hook-gi.repository.GLib.py
                - hook-gi.repository.GModule.py
                - hook-gi.repository.GObject.py
                - hook-gi.repository.Gdk.py
                - hook-gi.repository.GdkPixbuf.py
                - hook-gi.repository.Gio.py
                - hook-gi.repository.Graphene.py
                - hook-gi.repository.Gsk.py
                - hook-gi.repository.Gst.py
                - hook-gi.repository.GstAllocators.py
                - hook-gi.repository.GstApp.py
                - hook-gi.repository.GstAudio.py
                - hook-gi.repository.GstBadAudio.py
                - hook-gi.repository.GstBase.py
                - hook-gi.repository.GstCheck.py
                - hook-gi.repository.GstCodecs.py
                - hook-gi.repository.GstController.py
                - hook-gi.repository.GstGL.py
                - hook-gi.repository.GstGLEGL.py
                - hook-gi.repository.GstGLWayland.py
                - hook-gi.repository.GstGLX11.py
                - hook-gi.repository.GstInsertBin.py
                - hook-gi.repository.GstMpegts.py
                - hook-gi.repository.GstNet.py
                - hook-gi.repository.GstPbutils.py
                - hook-gi.repository.GstPlay.py
                - hook-gi.repository.GstPlayer.py
                - hook-gi.repository.GstRtp.py
                - hook-gi.repository.GstRtsp.py
                - hook-gi.repository.GstRtspServer.py
                - hook-gi.repository.GstSdp.py
                - hook-gi.repository.GstTag.py
                - hook-gi.repository.GstTranscoder.py
                - hook-gi.repository.GstVideo.py
                - hook-gi.repository.GstVulkan.py
                - hook-gi.repository.GstVulkanWayland.py
                - hook-gi.repository.GstVulkanXCB.py
                - hook-gi.repository.GstWebRTC.py
                - hook-gi.repository.Gtk.py
                - hook-gi.repository.GtkChamplain.py
                - hook-gi.repository.GtkClutter.py
                - hook-gi.repository.GtkSource.py
                - hook-gi.repository.GtkosxApplication.py
                - hook-gi.repository.HarfBuzz.py
                - hook-gi.repository.OsmGpsMap.py
                - hook-gi.repository.Pango.py
                - hook-gi.repository.PangoCairo.py
                - hook-gi.repository.Rsvg.py
                - hook-gi.repository.cairo.py
                - hook-gi.repository.freetype2.py
                - hook-gi.repository.xlib.py
                - hook-importlib_metadata.py
                - hook-importlib_resources.py
                - hook-inflect.py
                - hook-jaraco.context.py
                - hook-jaraco.functools.py
                - hook-jaraco.py
                - hook-jaraco.text.py
                - hook-more_itertools.py
                - hook-ordered_set.py
                - hook-packaging.py
                - hook-platformdirs.py
                - hook-setuptools.extern.six.moves.py
                - hook-six.moves.py
                - hook-tomli.py
                - hook-typeguard.py
                - hook-typing_extensions.py
                - hook-urllib3.packages.six.moves.py
                - hook-wheel.py
                - hook-zipp.py
                - **__pycache__/**
              - **rthooks/**
                - __init__.py
                - pyi_rth__tkinter.py
                - pyi_rth_django.py
                - pyi_rth_gdkpixbuf.py
                - pyi_rth_gi.py
                - pyi_rth_gio.py
                - pyi_rth_glib.py
                - pyi_rth_gstreamer.py
                - pyi_rth_gtk.py
                - pyi_rth_inspect.py
                - pyi_rth_kivy.py
                - pyi_rth_mplconfig.py
                - pyi_rth_multiprocessing.py
                - pyi_rth_pkgres.py
                - pyi_rth_pkgutil.py
                - pyi_rth_pyqt5.py
                - pyi_rth_pyqt6.py
                - pyi_rth_pyside2.py
                - pyi_rth_pyside6.py
                - pyi_rth_setuptools.py
                - **__pycache__/**
            - **isolated/**
              - __init__.py
              - _child.py
              - _parent.py
              - **__pycache__/**
            - **lib/**
              - README.rst
              - __init__.py
              - **__pycache__/**
              - **modulegraph/**
                - __init__.py
                - __main__.py
                - find_modules.py
                - modulegraph.py
                - util.py
                - **__pycache__/**
            - **loader/**
              - __init__.py
              - pyiboot01_bootstrap.py
              - pyimod01_archive.py
              - pyimod02_importers.py
              - pyimod03_ctypes.py
              - pyimod04_pywin32.py
              - **__pycache__/**
            - **utils/**
              - __init__.py
              - conftest.py
              - misc.py
              - osx.py
              - run_tests.py
              - tests.py
              - **__pycache__/**
              - **cliutils/**
                - __init__.py
                - archive_viewer.py
                - bindepend.py
                - grab_version.py
                - makespec.py
                - set_version.py
                - **__pycache__/**
              - **hooks/**
                - __init__.py
                - conda.py
                - django.py
                - gi.py
                - setuptools.py
                - tcl_tk.py
                - **__pycache__/**
                - **qt/**
                  - __init__.py
                  - _modules_info.py
                  - **__pycache__/**
              - **win32/**
                - __init__.py
                - icon.py
                - versioninfo.py
                - winmanifest.py
                - winresource.py
                - winutils.py
                - **__pycache__/**
          - **_distutils_hack/**
            - __init__.py
            - override.py
            - **__pycache__/**
          - **_pyinstaller_hooks_contrib/**
            - __init__.py
            - compat.py
            - rthooks.dat
            - **__pycache__/**
            - **pre_find_module_path/**
              - __init__.py
              - **__pycache__/**
            - **pre_safe_import_module/**
              - __init__.py
              - hook-tensorflow.py
              - hook-win32com.py
              - **__pycache__/**
            - **rthooks/**
              - __init__.py
              - pyi_rth_cryptography_openssl.py
              - pyi_rth_enchant.py
              - pyi_rth_ffpyplayer.py
              - pyi_rth_findlibs.py
              - pyi_rth_nltk.py
              - pyi_rth_osgeo.py
              - pyi_rth_pygraphviz.py
              - pyi_rth_pyproj.py
              - pyi_rth_pyqtgraph_multiprocess.py
              - pyi_rth_pythoncom.py
              - pyi_rth_pywintypes.py
              - pyi_rth_tensorflow.py
              - pyi_rth_traitlets.py
              - pyi_rth_usb.py
              - **__pycache__/**
            - **stdhooks/**
              - __init__.py
              - hook-BTrees.py
              - hook-CTkMessagebox.py
              - hook-Crypto.py
              - hook-Cryptodome.py
              - hook-HtmlTestRunner.py
              - hook-IPython.py
              - hook-OpenGL.py
              - hook-OpenGL_accelerate.py
              - hook-PyTaskbar.py
              - hook-Xlib.py
              - hook-_mssql.py
              - hook-_mysql.py
              - hook-accessible_output2.py
              - hook-adbc_driver_manager.py
              - hook-adbutils.py
              - hook-adios.py
              - hook-afmformats.py
              - hook-aliyunsdkcore.py
              - hook-altair.py
              - hook-amazonproduct.py
              - hook-anyio.py
              - hook-apkutils.py
              - hook-appdirs.py
              - hook-appy.pod.py
              - hook-apscheduler.py
              - hook-argon2.py
              - hook-astor.py
              - hook-astroid.py
              - hook-astropy.py
              - hook-astropy_iers_data.py
              - hook-av.py
              - hook-avro.py
              - hook-azurerm.py
              - hook-backports.py
              - hook-backports.zoneinfo.py
              - hook-bacon.py
              - hook-bcrypt.py
              - hook-bitsandbytes.py
              - hook-black.py
              - hook-bleak.py
              - hook-blib2to3.py
              - hook-blspy.py
              - hook-bokeh.py
              - hook-boto.py
              - hook-boto3.py
              - hook-botocore.py
              - hook-branca.py
              - hook-cairocffi.py
              - hook-cairosvg.py
              - hook-capstone.py
              - hook-cassandra.py
              - hook-celpy.py
              - hook-certifi.py
              - hook-cf_units.py
              - hook-cftime.py
              - hook-charset_normalizer.py
              - hook-cloudpickle.py
              - hook-cloudscraper.py
              - hook-clr.py
              - hook-clr_loader.py
              - hook-cmocean.py
              - hook-compliance_checker.py
              - hook-comtypes.client.py
              - hook-countrycode.py
              - hook-countryinfo.py
              - hook-cryptography.py
              - hook-cumm.py
              - hook-customtkinter.py
              - hook-cv2.py
              - hook-cx_Oracle.py
              - hook-cytoolz.itertoolz.py
              - hook-dash.py
              - hook-dash_bootstrap_components.py
              - hook-dash_core_components.py
              - hook-dash_html_components.py
              - hook-dash_renderer.py
              - hook-dash_table.py
              - hook-dash_uploader.py
              - hook-dask.py
              - hook-datasets.py
              - hook-dateparser.py
              - hook-dateparser.utils.strptime.py
              - hook-dateutil.py
              - hook-dbus_fast.py
              - hook-dclab.py
              - hook-ddgs.py
              - hook-detectron2.py
              - hook-discid.py
              - hook-distorm3.py
              - hook-distributed.py
              - hook-dns.rdata.py
              - hook-docutils.py
              - hook-docx.py
              - hook-docx2pdf.py
              - hook-duckdb.py
              - hook-dynaconf.py
              - hook-easyocr.py
              - hook-eccodeslib.py
              - hook-eckitlib.py
              - hook-eel.py
              - hook-emoji.py
              - hook-enchant.py
              - hook-eng_to_ipa.py
              - hook-ens.py
              - hook-enzyme.parsers.ebml.core.py
              - hook-eth_abi.py
              - hook-eth_account.py
              - hook-eth_hash.py
              - hook-eth_keyfile.py
              - hook-eth_keys.py
              - hook-eth_rlp.py
              - hook-eth_typing.py
              - hook-eth_utils.network.py
              - hook-eth_utils.py
              - hook-exchangelib.py
              - hook-fabric.py
              - hook-fairscale.py
              - hook-fake_useragent.py
              - hook-faker.py
              - hook-falcon.py
              - hook-fastai.py
              - hook-fastparquet.py
              - hook-fckitlib.py
              - hook-ffpyplayer.py
              - hook-fiona.py
              - hook-flask_compress.py
              - hook-flask_restx.py
              - hook-flex.py
              - hook-flirpy.py
              - hook-fmpy.py
              - hook-folium.py
              - hook-freetype.py
              - hook-frictionless.py
              - hook-fsspec.py
              - hook-fvcore.nn.py
              - hook-gadfly.py
              - hook-gbulb.py
              - hook-gcloud.py
              - hook-geopandas.py
              - hook-gitlab.py
              - hook-globus_sdk.py
              - hook-gmplot.py
              - hook-gmsh.py
              - hook-gooey.py
              - hook-google.api_core.py
              - hook-google.cloud.bigquery.py
              - hook-google.cloud.core.py
              - hook-google.cloud.kms_v1.py
              - hook-google.cloud.pubsub_v1.py
              - hook-google.cloud.speech.py
              - hook-google.cloud.storage.py
              - hook-google.cloud.translate.py
              - hook-googleapiclient.model.py
              - hook-grapheme.py
              - hook-graphql_query.py
              - hook-great_expectations.py
              - hook-gribapi.py
              - hook-grpc.py
              - hook-gtk.py
              - hook-h3.py
              - hook-h5py.py
              - hook-hdf5plugin.py
              - hook-hexbytes.py
              - hook-httplib2.py
              - hook-humanize.py
              - hook-hydra.py
              - hook-ijson.py
              - hook-imageio.py
              - hook-imageio_ffmpeg.py
              - hook-iminuit.py
              - hook-intake.py
              - hook-iso639.py
              - hook-itk.py
              - hook-jaraco.text.py
              - hook-jedi.py
              - hook-jieba.py
              - hook-jinja2.py
              - hook-jinxed.py
              - hook-jira.py
              - hook-jsonpath_rw_ext.py
              - hook-jsonrpcserver.py
              - hook-jsonschema.py
              - hook-jsonschema_specifications.py
              - hook-jupyterlab.py
              - hook-kaleido.py
              - hook-khmernltk.py
              - hook-kinterbasdb.py
              - hook-langchain.py
              - hook-langchain_classic.py
              - hook-langcodes.py
              - hook-langdetect.py
              - hook-laonlp.py
              - hook-lark.py
              - hook-ldfparser.py
              - hook-lensfunpy.py
              - hook-libaudioverse.py
              - hook-librosa.py
              - hook-lightgbm.py
              - hook-lightning.py
              - hook-limits.py
              - hook-linear_operator.py
              - hook-lingua.py
              - hook-litestar.py
              - hook-llvmlite.py
              - hook-logilab.py
              - hook-lxml.etree.py
              - hook-lxml.isoschematron.py
              - hook-lxml.objectify.py
              - hook-lxml.py
              - hook-lz4.py
              - hook-magic.py
              - hook-mako.codegen.py
              - hook-mariadb.py
              - hook-markdown.py
              - hook-mecab.py
              - hook-metpy.py
              - hook-migrate.py
              - hook-mimesis.py
              - hook-minecraft_launcher_lib.py
              - hook-mistune.py
              - hook-mnemonic.py
              - hook-monai.py
              - hook-moviepy.audio.fx.all.py
              - hook-moviepy.video.fx.all.py
              - hook-mpl_toolkits.basemap.py
              - hook-msoffcrypto.py
              - hook-nacl.py
              - hook-names.py
              - hook-nanite.py
              - hook-narwhals.py
              - hook-nbconvert.py
              - hook-nbdime.py
              - hook-nbformat.py
              - hook-nbt.py
              - hook-ncclient.py
              - hook-netCDF4.py
              - hook-nicegui.py
              - hook-niquests.py
              - hook-nltk.py
              - hook-nnpy.py
              - hook-notebook.py
              - hook-numba.py
              - hook-numbers_parser.py
              - hook-numcodecs.py
              - hook-nvidia.cublas.py
              - hook-nvidia.cuda_cupti.py
              - hook-nvidia.cuda_nvcc.py
              - hook-nvidia.cuda_nvrtc.py
              - hook-nvidia.cuda_runtime.py
              - hook-nvidia.cudnn.py
              - hook-nvidia.cufft.py
              - hook-nvidia.curand.py
              - hook-nvidia.cusolver.py
              - hook-nvidia.cusparse.py
              - hook-nvidia.nccl.py
              - hook-nvidia.nvjitlink.py
              - hook-nvidia.nvtx.py
              - hook-office365.py
              - hook-onnxruntime.py
              - hook-opencc.py
              - hook-openpyxl.py
              - hook-opentelemetry.py
              - hook-orjson.py
              - hook-osgeo.py
              - hook-pandas_flavor.py
              - hook-panel.py
              - hook-parsedatetime.py
              - hook-parso.py
              - hook-passlib.py
              - hook-paste.exceptions.reporter.py
              - hook-patoolib.py
              - hook-patsy.py
              - hook-pdfminer.py
              - hook-pendulum.py
              - hook-phonenumbers.py
              - hook-pingouin.py
              - hook-pint.py
              - hook-pinyin.py
              - hook-platformdirs.py
              - hook-plotly.py
              - hook-pointcept.py
              - hook-pptx.py
              - hook-prettytable.py
              - hook-psutil.py
              - hook-psychopy.py
              - hook-psycopg2.py
              - hook-psycopg_binary.py
              - hook-publicsuffix2.py
              - hook-pubsub.core.py
              - hook-puremagic.py
              - hook-py.py
              - hook-pyarrow.py
              - hook-pycountry.py
              - hook-pycparser.py
              - hook-pycrfsuite.py
              - hook-pydantic.py
              - hook-pydicom.py
              - hook-pydivert.py
              - hook-pyecharts.py
              - hook-pyexcel-io.py
              - hook-pyexcel-ods.py
              - hook-pyexcel-ods3.py
              - hook-pyexcel-odsr.py
              - hook-pyexcel-xls.py
              - hook-pyexcel-xlsx.py
              - hook-pyexcel-xlsxw.py
              - hook-pyexcel.py
              - hook-pyexcel_io.py
              - hook-pyexcel_ods.py
              - hook-pyexcel_ods3.py
              - hook-pyexcel_odsr.py
              - hook-pyexcel_xls.py
              - hook-pyexcel_xlsx.py
              - hook-pyexcel_xlsxw.py
              - hook-pyexcelerate.Writer.py
              - hook-pygraphviz.py
              - hook-pygwalker.py
              - hook-pylibmagic.py
              - hook-pylint.py
              - hook-pylsl.py
              - hook-pymediainfo.py
              - hook-pymeshlab.py
              - hook-pymorphy3.py
              - hook-pymssql.py
              - hook-pynng.py
              - hook-pynput.py
              - hook-pyodbc.py
              - hook-pyopencl.py
              - hook-pypdfium2.py
              - hook-pypdfium2_raw.py
              - hook-pypemicro.py
              - hook-pyphen.py
              - hook-pyppeteer.py
              - hook-pyproj.py
              - hook-pypsexec.py
              - hook-pypylon.py
              - hook-pyqtgraph.py
              - hook-pyshark.py
              - hook-pysnmp.py
              - hook-pystray.py
              - hook-pytest.py
              - hook-pythainlp.py
              - hook-pythoncom.py
              - hook-pytokens.py
              - hook-pyttsx.py
              - hook-pyttsx3.py
              - hook-pyviz_comms.py
              - hook-pyvjoy.py
              - hook-pywintypes.py
              - hook-pywt.py
              - hook-qtmodern.py
              - hook-radicale.py
              - hook-raven.py
              - hook-rawpy.py
              - hook-rdflib.py
              - hook-redmine.py
              - hook-regex.py
              - hook-reportlab.lib.utils.py
              - hook-reportlab.pdfbase._fontdata.py
              - hook-resampy.py
              - hook-rich.py
              - hook-rlp.py
              - hook-rpy2.py
              - hook-rtree.py
              - hook-ruamel.yaml.py
              - hook-rubicon.py
              - hook-sacremoses.py
              - hook-sam2.py
              - hook-saml2.py
              - hook-schwifty.py
              - hook-seedir.py
              - hook-selectolax.py
              - hook-selenium.py
              - hook-sentry_sdk.py
              - hook-setuptools_scm.py
              - hook-shapely.py
              - hook-shotgun_api3.py
              - hook-simplemma.py
              - hook-skimage.color.py
              - hook-skimage.data.py
              - hook-skimage.draw.py
              - hook-skimage.exposure.py
              - hook-skimage.feature.py
              - hook-skimage.filters.py
              - hook-skimage.future.py
              - hook-skimage.graph.py
              - hook-skimage.io.py
              - hook-skimage.measure.py
              - hook-skimage.metrics.py
              - hook-skimage.morphology.py
              - hook-skimage.py
              - hook-skimage.registration.py
              - hook-skimage.restoration.py
              - hook-skimage.segmentation.py
              - hook-skimage.transform.py
              - hook-sklearn.cluster.py
              - hook-sklearn.externals.array_api_compat.cupy.py
              - hook-sklearn.externals.array_api_compat.dask.array.py
              - hook-sklearn.externals.array_api_compat.numpy.py
              - hook-sklearn.externals.array_api_compat.torch.py
              - hook-sklearn.linear_model.py
              - hook-sklearn.metrics.cluster.py
              - hook-sklearn.metrics.pairwise.py
              - hook-sklearn.metrics.py
              - hook-sklearn.neighbors.py
              - hook-sklearn.py
              - hook-sklearn.tree.py
              - hook-sklearn.utils.py
              - hook-skyfield.py
              - hook-slixmpp.py
              - hook-sound_lib.py
              - hook-sounddevice.py
              - hook-soundfile.py
              - hook-spacy.py
              - hook-speech_recognition.py
              - hook-spiceypy.py
              - hook-spnego.py
              - hook-srsly.msgpack._packer.py
              - hook-sspilib.raw.py
              - hook-statsmodels.tsa.statespace.py
              - hook-stdnum.py
              - hook-storm.database.py
              - hook-sudachipy.py
              - hook-sunpy.py
              - hook-sv_ttk.py
              - hook-swagger_spec_validator.py
              - hook-tableauhyperapi.py
              - hook-tables.py
              - hook-tcod.py
              - hook-tensorflow.py
              - hook-text_unidecode.py
              - hook-textdistance.py
              - hook-thinc.backends.numpy_ops.py
              - hook-thinc.py
              - hook-timezonefinder.py
              - hook-timm.py
              - hook-tinycss2.py
              - hook-tkinterdnd2.py
              - hook-tkinterweb.py
              - hook-tkinterweb_tkhtml.py
              - hook-tkinterweb_tkhtml_extras.py
              - hook-toga.py
              - hook-toga_cocoa.py
              - hook-toga_gtk.py
              - hook-toga_winforms.py
              - hook-torch.py
              - hook-torchao.py
              - hook-torchaudio.py
              - hook-torchtext.py
              - hook-torchvision.io.image.py
              - hook-torchvision.py
              - hook-trame.py
              - hook-trame_client.py
              - hook-trame_code.py
              - hook-trame_components.py
              - hook-trame_datagrid.py
              - hook-trame_deckgl.py
              - hook-trame_formkit.py
              - hook-trame_grid.py
              - hook-trame_iframe.py
              - hook-trame_keycloak.py
              - hook-trame_leaflet.py
              - hook-trame_markdown.py
              - hook-trame_matplotlib.py
              - hook-trame_mesh_streamer.py
              - hook-trame_plotly.py
              - hook-trame_pvui.py
              - hook-trame_quasar.py
              - hook-trame_rca.py
              - hook-trame_router.py
              - hook-trame_simput.py
              - hook-trame_tauri.py
              - hook-trame_tweakpane.py
              - hook-trame_vega.py
              - hook-trame_vtk.py
              - hook-trame_vtk3d.py
              - hook-trame_vtklocal.py
              - hook-trame_vuetify.py
              - hook-trame_xterm.py
              - hook-transformers.py
              - hook-travertino.py
              - hook-trimesh.py
              - hook-triton.py
              - hook-ttkthemes.py
              - hook-ttkwidgets.py
              - hook-tzdata.py
              - hook-tzwhere.py
              - hook-u1db.py
              - hook-ultralytics.py
              - hook-umap.py
              - hook-unidecode.py
              - hook-uniseg.py
              - hook-urllib3.py
              - hook-urllib3_future.py
              - hook-usb.py
              - hook-uuid6.py
              - hook-uvicorn.py
              - hook-uvloop.py
              - hook-vaderSentiment.py
              - hook-vtkmodules.vtkAcceleratorsVTKmCore.py
              - hook-vtkmodules.vtkAcceleratorsVTKmDataModel.py
              - hook-vtkmodules.vtkAcceleratorsVTKmFilters.py
              - hook-vtkmodules.vtkChartsCore.py
              - hook-vtkmodules.vtkCommonColor.py
              - hook-vtkmodules.vtkCommonComputationalGeometry.py
              - hook-vtkmodules.vtkCommonDataModel.py
              - hook-vtkmodules.vtkCommonExecutionModel.py
              - hook-vtkmodules.vtkCommonMath.py
              - hook-vtkmodules.vtkCommonMisc.py
              - hook-vtkmodules.vtkCommonPython.py
              - hook-vtkmodules.vtkCommonSystem.py
              - hook-vtkmodules.vtkCommonTransforms.py
              - hook-vtkmodules.vtkDomainsChemistry.py
              - hook-vtkmodules.vtkDomainsChemistryOpenGL2.py
              - hook-vtkmodules.vtkFiltersAMR.py
              - hook-vtkmodules.vtkFiltersCellGrid.py
              - hook-vtkmodules.vtkFiltersCore.py
              - hook-vtkmodules.vtkFiltersExtraction.py
              - hook-vtkmodules.vtkFiltersFlowPaths.py
              - hook-vtkmodules.vtkFiltersGeneral.py
              - hook-vtkmodules.vtkFiltersGeneric.py
              - hook-vtkmodules.vtkFiltersGeometry.py
              - hook-vtkmodules.vtkFiltersGeometryPreview.py
              - hook-vtkmodules.vtkFiltersHybrid.py
              - hook-vtkmodules.vtkFiltersHyperTree.py
              - hook-vtkmodules.vtkFiltersImaging.py
              - hook-vtkmodules.vtkFiltersModeling.py
              - hook-vtkmodules.vtkFiltersParallel.py
              - hook-vtkmodules.vtkFiltersParallelDIY2.py
              - hook-vtkmodules.vtkFiltersParallelImaging.py
              - hook-vtkmodules.vtkFiltersParallelStatistics.py
              - hook-vtkmodules.vtkFiltersPoints.py
              - hook-vtkmodules.vtkFiltersProgrammable.py
              - hook-vtkmodules.vtkFiltersPython.py
              - hook-vtkmodules.vtkFiltersReduction.py
              - hook-vtkmodules.vtkFiltersSMP.py
              - hook-vtkmodules.vtkFiltersSelection.py
              - hook-vtkmodules.vtkFiltersSources.py
              - hook-vtkmodules.vtkFiltersStatistics.py
              - hook-vtkmodules.vtkFiltersTemporal.py
              - hook-vtkmodules.vtkFiltersTensor.py
              - hook-vtkmodules.vtkFiltersTexture.py
              - hook-vtkmodules.vtkFiltersTopology.py
              - hook-vtkmodules.vtkFiltersVerdict.py
              - hook-vtkmodules.vtkGeovisCore.py
              - hook-vtkmodules.vtkIOAMR.py
              - hook-vtkmodules.vtkIOAsynchronous.py
              - hook-vtkmodules.vtkIOAvmesh.py
              - hook-vtkmodules.vtkIOCGNSReader.py
              - hook-vtkmodules.vtkIOCONVERGECFD.py
              - hook-vtkmodules.vtkIOCellGrid.py
              - hook-vtkmodules.vtkIOCesium3DTiles.py
              - hook-vtkmodules.vtkIOChemistry.py
              - hook-vtkmodules.vtkIOCityGML.py
              - hook-vtkmodules.vtkIOCore.py
              - hook-vtkmodules.vtkIOERF.py
              - hook-vtkmodules.vtkIOEnSight.py
              - hook-vtkmodules.vtkIOEngys.py
              - hook-vtkmodules.vtkIOExodus.py
              - hook-vtkmodules.vtkIOExport.py
              - hook-vtkmodules.vtkIOExportGL2PS.py
              - hook-vtkmodules.vtkIOExportPDF.py
              - hook-vtkmodules.vtkIOFDS.py
              - hook-vtkmodules.vtkIOFLUENTCFF.py
              - hook-vtkmodules.vtkIOGeoJSON.py
              - hook-vtkmodules.vtkIOGeometry.py
              - hook-vtkmodules.vtkIOH5Rage.py
              - hook-vtkmodules.vtkIOH5part.py
              - hook-vtkmodules.vtkIOHDF.py
              - hook-vtkmodules.vtkIOIOSS.py
              - hook-vtkmodules.vtkIOImage.py
              - hook-vtkmodules.vtkIOImport.py
              - hook-vtkmodules.vtkIOInfovis.py
              - hook-vtkmodules.vtkIOLANLX3D.py
              - hook-vtkmodules.vtkIOLSDyna.py
              - hook-vtkmodules.vtkIOLegacy.py
              - hook-vtkmodules.vtkIOMINC.py
              - hook-vtkmodules.vtkIOMotionFX.py
              - hook-vtkmodules.vtkIOMovie.py
              - hook-vtkmodules.vtkIONetCDF.py
              - hook-vtkmodules.vtkIOOMF.py
              - hook-vtkmodules.vtkIOOggTheora.py
              - hook-vtkmodules.vtkIOPIO.py
              - hook-vtkmodules.vtkIOPLY.py
              - hook-vtkmodules.vtkIOParallel.py
              - hook-vtkmodules.vtkIOParallelExodus.py
              - hook-vtkmodules.vtkIOParallelLSDyna.py
              - hook-vtkmodules.vtkIOParallelXML.py
              - hook-vtkmodules.vtkIOSQL.py
              - hook-vtkmodules.vtkIOSegY.py
              - hook-vtkmodules.vtkIOTRUCHAS.py
              - hook-vtkmodules.vtkIOTecplotTable.py
              - hook-vtkmodules.vtkIOVPIC.py
              - hook-vtkmodules.vtkIOVeraOut.py
              - hook-vtkmodules.vtkIOVideo.py
              - hook-vtkmodules.vtkIOXML.py
              - hook-vtkmodules.vtkIOXMLParser.py
              - hook-vtkmodules.vtkIOXdmf2.py
              - hook-vtkmodules.vtkImagingColor.py
              - hook-vtkmodules.vtkImagingCore.py
              - hook-vtkmodules.vtkImagingFourier.py
              - hook-vtkmodules.vtkImagingGeneral.py
              - hook-vtkmodules.vtkImagingHybrid.py
              - hook-vtkmodules.vtkImagingMath.py
              - hook-vtkmodules.vtkImagingMorphological.py
              - hook-vtkmodules.vtkImagingOpenGL2.py
              - hook-vtkmodules.vtkImagingSources.py
              - hook-vtkmodules.vtkImagingStatistics.py
              - hook-vtkmodules.vtkImagingStencil.py
              - hook-vtkmodules.vtkInfovisCore.py
              - hook-vtkmodules.vtkInfovisLayout.py
              - hook-vtkmodules.vtkInteractionImage.py
              - hook-vtkmodules.vtkInteractionStyle.py
              - hook-vtkmodules.vtkInteractionWidgets.py
              - hook-vtkmodules.vtkParallelCore.py
              - hook-vtkmodules.vtkPythonContext2D.py
              - hook-vtkmodules.vtkRenderingAnnotation.py
              - hook-vtkmodules.vtkRenderingCellGrid.py
              - hook-vtkmodules.vtkRenderingContext2D.py
              - hook-vtkmodules.vtkRenderingContextOpenGL2.py
              - hook-vtkmodules.vtkRenderingCore.py
              - hook-vtkmodules.vtkRenderingExternal.py
              - hook-vtkmodules.vtkRenderingFreeType.py
              - hook-vtkmodules.vtkRenderingGL2PSOpenGL2.py
              - hook-vtkmodules.vtkRenderingGridAxes.py
              - hook-vtkmodules.vtkRenderingHyperTreeGrid.py
              - hook-vtkmodules.vtkRenderingImage.py
              - hook-vtkmodules.vtkRenderingLICOpenGL2.py
              - hook-vtkmodules.vtkRenderingLOD.py
              - hook-vtkmodules.vtkRenderingLabel.py
              - hook-vtkmodules.vtkRenderingMatplotlib.py
              - hook-vtkmodules.vtkRenderingOpenGL2.py
              - hook-vtkmodules.vtkRenderingParallel.py
              - hook-vtkmodules.vtkRenderingSceneGraph.py
              - hook-vtkmodules.vtkRenderingUI.py
              - hook-vtkmodules.vtkRenderingVR.py
              - hook-vtkmodules.vtkRenderingVRModels.py
              - hook-vtkmodules.vtkRenderingVolume.py
              - hook-vtkmodules.vtkRenderingVolumeAMR.py
              - hook-vtkmodules.vtkRenderingVolumeOpenGL2.py
              - hook-vtkmodules.vtkRenderingVtkJS.py
              - hook-vtkmodules.vtkSerializationManager.py
              - hook-vtkmodules.vtkTestingRendering.py
              - hook-vtkmodules.vtkTestingSerialization.py
              - hook-vtkmodules.vtkViewsContext2D.py
              - hook-vtkmodules.vtkViewsCore.py
              - hook-vtkmodules.vtkViewsInfovis.py
              - hook-vtkmodules.vtkWebCore.py
              - hook-vtkmodules.vtkWebGLExporter.py
              - hook-vtkpython.py
              - hook-wavefile.py
              - hook-weasyprint.py
              - hook-web3.py
              - hook-webassets.py
              - hook-webrtcvad.py
              - hook-websockets.py
              - hook-webview.py
              - hook-win32com.py
              - hook-wordcloud.py
              - hook-workflow.py
              - hook-wx.lib.activex.py
              - hook-wx.lib.pubsub.py
              - hook-wx.xrc.py
              - hook-xarray.py
              - hook-xml.dom.html.HTMLDocument.py
              - hook-xml.sax.saxexts.py
              - hook-xmldiff.py
              - hook-xmlschema.py
              - hook-xsge_gui.py
              - hook-xyzservices.py
              - hook-yapf_third_party.py
              - hook-z3c.rml.py
              - hook-zarr.py
              - hook-zeep.py
              - hook-zmq.py
              - hook-zoneinfo.py
              - **__pycache__/**
            - **utils/**
              - __init__.py
              - mypy.py
              - nvidia_cuda.py
              - vtkmodules.py
              - **__pycache__/**
          - **altgraph/**
            - Dot.py
            - Graph.py
            - GraphAlgo.py
            - GraphStat.py
            - GraphUtil.py
            - ObjectGraph.py
            - __init__.py
          - **altgraph-0.17.5.dist-info/**
            - INSTALLER
            - LICENSE
            - METADATA
            - RECORD
            - WHEEL
            - top_level.txt
            - zip-safe
            - **__pycache__/**
          - **bidict/**
            - __init__.py
            - _abc.py
            - _base.py
            - _bidict.py
            - _dup.py
            - _exc.py
            - _frozen.py
            - _iter.py
            - _orderedbase.py
            - _orderedbidict.py
            - _typing.py
            - metadata.py
            - py.typed
          - **bidict-0.23.1.dist-info/**
            - INSTALLER
            - LICENSE
            - METADATA
            - RECORD
            - WHEEL
            - top_level.txt
            - **__pycache__/**
          - **blinker/**
            - __init__.py
            - _utilities.py
            - base.py
            - py.typed
          - **blinker-1.9.0.dist-info/**
            - INSTALLER
            - LICENSE.txt
            - METADATA
            - RECORD
            - WHEEL
            - **__pycache__/**
          - **click/**
            - __init__.py
            - _compat.py
            - _termui_impl.py
            - _textwrap.py
            - _utils.py
            - _winconsole.py
            - core.py
            - decorators.py
            - exceptions.py
            - formatting.py
            - globals.py
            - parser.py
            - py.typed
            - shell_completion.py
            - termui.py
            - testing.py
            - types.py
            - utils.py
          - **click-8.3.1.dist-info/**
            - INSTALLER
            - METADATA
            - RECORD
            - WHEEL
            - **licenses/**
              - LICENSE.txt
            - **__pycache__/**
          - **dns/**
            - __init__.py
            - _asyncbackend.py
            - _asyncio_backend.py
            - _ddr.py
            - _features.py
            - _immutable_ctx.py
            - _no_ssl.py
            - _tls_util.py
            - _trio_backend.py
            - asyncbackend.py
            - asyncquery.py
            - asyncresolver.py
            - btree.py
            - btreezone.py
            - dnssec.py
            - dnssectypes.py
            - e164.py
            - edns.py
            - entropy.py
            - enum.py
            - exception.py
            - flags.py
            - grange.py
            - immutable.py
            - inet.py
            - ipv4.py
            - ipv6.py
            - message.py
            - name.py
            - namedict.py
            - nameserver.py
            - node.py
            - opcode.py
            - py.typed
            - query.py
            - rcode.py
            - rdata.py
            - rdataclass.py
            - rdataset.py
            - rdatatype.py
            - renderer.py
            - resolver.py
            - reversename.py
            - rrset.py
            - serial.py
            - set.py
            - tokenizer.py
            - transaction.py
            - tsig.py
            - tsigkeyring.py
            - ttl.py
            - update.py
            - version.py
            - versioned.py
            - win32util.py
            - wire.py
            - xfr.py
            - zone.py
            - zonefile.py
            - zonetypes.py
            - **__pycache__/**
            - **dnssecalgs/**
              - __init__.py
              - base.py
              - cryptography.py
              - dsa.py
              - ecdsa.py
              - eddsa.py
              - rsa.py
              - **__pycache__/**
            - **quic/**
              - __init__.py
              - _asyncio.py
              - _common.py
              - _sync.py
              - _trio.py
              - **__pycache__/**
            - **rdtypes/**
              - __init__.py
              - dnskeybase.py
              - dsbase.py
              - euibase.py
              - mxbase.py
              - nsbase.py
              - svcbbase.py
              - tlsabase.py
              - txtbase.py
              - util.py
              - **ANY/**
                - AFSDB.py
                - AMTRELAY.py
                - AVC.py
                - CAA.py
                - CDNSKEY.py
                - CDS.py
                - CERT.py
                - CNAME.py
                - CSYNC.py
                - DLV.py
                - DNAME.py
                - DNSKEY.py
                - DS.py
                - DSYNC.py
                - EUI48.py
                - EUI64.py
                - GPOS.py
                - HINFO.py
                - HIP.py
                - ISDN.py
                - L32.py
                - L64.py
                - LOC.py
                - LP.py
                - MX.py
                - NID.py
                - NINFO.py
                - NS.py
                - NSEC.py
                - NSEC3.py
                - NSEC3PARAM.py
                - OPENPGPKEY.py
                - OPT.py
                - PTR.py
                - RESINFO.py
                - RP.py
                - RRSIG.py
                - RT.py
                - SMIMEA.py
                - SOA.py
                - SPF.py
                - SSHFP.py
                - TKEY.py
                - TLSA.py
                - TSIG.py
                - TXT.py
                - URI.py
                - WALLET.py
                - X25.py
                - ZONEMD.py
                - __init__.py
                - **__pycache__/**
              - **CH/**
                - A.py
                - __init__.py
                - **__pycache__/**
              - **IN/**
                - A.py
                - AAAA.py
                - APL.py
                - DHCID.py
                - HTTPS.py
                - IPSECKEY.py
                - KX.py
                - NAPTR.py
                - NSAP.py
                - NSAP_PTR.py
                - PX.py
                - SRV.py
                - SVCB.py
                - WKS.py
                - __init__.py
                - **__pycache__/**
              - **__pycache__/**
          - **dnspython-2.8.0.dist-info/**
            - INSTALLER
            - METADATA
            - RECORD
            - WHEEL
            - **licenses/**
              - LICENSE
          - **engineio/**
            - __init__.py
            - async_client.py
            - async_server.py
            - async_socket.py
            - base_client.py
            - base_server.py
            - base_socket.py
            - client.py
            - exceptions.py
            - json.py
            - middleware.py
            - packet.py
            - payload.py
            - server.py
            - socket.py
            - static_files.py
            - **__pycache__/**
            - **async_drivers/**
              - __init__.py
              - _websocket_wsgi.py
              - aiohttp.py
              - asgi.py
              - eventlet.py
              - gevent.py
              - gevent_uwsgi.py
              - sanic.py
              - threading.py
              - tornado.py
              - **__pycache__/**
          - **eventlet/**
            - __init__.py
            - _version.py
            - asyncio.py
            - backdoor.py
            - convenience.py
            - corolocal.py
            - coros.py
            - dagpool.py
            - db_pool.py
            - debug.py
            - event.py
            - greenpool.py
            - greenthread.py
            - lock.py
            - patcher.py
            - pools.py
            - queue.py
            - semaphore.py
            - timeout.py
            - tpool.py
            - websocket.py
            - wsgi.py
          - **eventlet-0.40.4.dist-info/**
            - INSTALLER
            - METADATA
            - RECORD
            - REQUESTED
            - WHEEL
            - **licenses/**
              - AUTHORS
              - LICENSE
            - **__pycache__/**
            - **green/**
              - BaseHTTPServer.py
              - CGIHTTPServer.py
              - MySQLdb.py
              - Queue.py
              - SimpleHTTPServer.py
              - SocketServer.py
              - __init__.py
              - _socket_nodns.py
              - asynchat.py
              - asyncore.py
              - builtin.py
              - ftplib.py
              - httplib.py
              - os.py
              - profile.py
              - select.py
              - selectors.py
              - socket.py
              - ssl.py
              - subprocess.py
              - thread.py
              - threading.py
              - time.py
              - urllib2.py
              - zmq.py
              - **OpenSSL/**
                - SSL.py
                - __init__.py
                - crypto.py
                - tsafe.py
                - version.py
                - **__pycache__/**
              - **__pycache__/**
              - **http/**
                - __init__.py
                - client.py
                - cookiejar.py
                - cookies.py
                - server.py
                - **__pycache__/**
              - **urllib/**
                - __init__.py
                - error.py
                - parse.py
                - request.py
                - response.py
                - **__pycache__/**
            - **greenio/**
              - __init__.py
              - base.py
              - py3.py
              - **__pycache__/**
            - **hubs/**
              - __init__.py
              - asyncio.py
              - epolls.py
              - hub.py
              - kqueue.py
              - poll.py
              - pyevent.py
              - selects.py
              - timer.py
              - **__pycache__/**
            - **support/**
              - __init__.py
              - greendns.py
              - greenlets.py
              - psycopg2_patcher.py
              - pylib.py
              - stacklesspypys.py
              - stacklesss.py
              - **__pycache__/**
            - **zipkin/**
              - README.rst
              - __init__.py
              - api.py
              - client.py
              - greenthread.py
              - http.py
              - log.py
              - patcher.py
              - wsgi.py
              - **__pycache__/**
              - **_thrift/**
                - README.rst
                - __init__.py
                - zipkinCore.thrift
                - **__pycache__/**
                - **zipkinCore/**
                  - __init__.py
                  - constants.py
                  - ttypes.py
                  - **__pycache__/**
              - **example/**
                - ex1.png
                - ex2.png
                - ex3.png
          - **flask/**
            - __init__.py
            - __main__.py
            - app.py
            - blueprints.py
            - cli.py
            - config.py
            - ctx.py
            - debughelpers.py
            - globals.py
            - helpers.py
            - logging.py
            - py.typed
            - sessions.py
            - signals.py
            - templating.py
            - testing.py
            - typing.py
            - views.py
            - wrappers.py
          - **flask-3.1.3.dist-info/**
            - INSTALLER
            - METADATA
            - RECORD
            - REQUESTED
            - WHEEL
            - entry_points.txt
            - **licenses/**
              - LICENSE.txt
            - **__pycache__/**
            - **json/**
              - __init__.py
              - provider.py
              - tag.py
              - **__pycache__/**
            - **sansio/**
              - README.md
              - app.py
              - blueprints.py
              - scaffold.py
              - **__pycache__/**
          - **flask_jwt_extended/**
            - __init__.py
            - config.py
            - default_callbacks.py
            - exceptions.py
            - internal_utils.py
            - jwt_manager.py
            - py.typed
            - tokens.py
            - typing.py
            - utils.py
            - view_decorators.py
            - **__pycache__/**
          - **flask_login/**
            - __about__.py
            - __init__.py
            - config.py
            - login_manager.py
            - mixins.py
            - signals.py
            - test_client.py
            - utils.py
            - **__pycache__/**
          - **flask_socketio/**
            - __init__.py
            - namespace.py
            - test_client.py
          - **flask_socketio-5.6.1.dist-info/**
            - INSTALLER
            - METADATA
            - RECORD
            - REQUESTED
            - WHEEL
            - top_level.txt
            - **licenses/**
              - LICENSE
            - **__pycache__/**
          - **greenlet/**
            - CObjects.cpp
            - PyGreenlet.cpp
            - PyGreenlet.hpp
            - PyGreenletUnswitchable.cpp
            - PyModule.cpp
            - TBrokenGreenlet.cpp
            - TExceptionState.cpp
            - TGreenlet.cpp
            - TGreenlet.hpp
            - TGreenletGlobals.cpp
            - TMainGreenlet.cpp
            - TPythonState.cpp
            - TStackState.cpp
            - TThreadState.hpp
            - TThreadStateCreator.hpp
            - TThreadStateDestroy.cpp
            - TUserGreenlet.cpp
            - __init__.py
            - _greenlet.cpython-310-x86_64-linux-gnu.so
            - greenlet.cpp
            - greenlet.h
            - greenlet_allocator.hpp
            - greenlet_compiler_compat.hpp
            - greenlet_cpython_compat.hpp
            - greenlet_exceptions.hpp
            - greenlet_internal.hpp
            - greenlet_msvc_compat.hpp
            - greenlet_refs.hpp
            - greenlet_slp_switch.hpp
            - greenlet_thread_support.hpp
            - slp_platformselect.h
          - **greenlet-3.3.2.dist-info/**
            - INSTALLER
            - METADATA
            - RECORD
            - WHEEL
            - top_level.txt
            - **licenses/**
              - LICENSE
              - LICENSE.PSF
            - **__pycache__/**
            - **platform/**
              - __init__.py
              - setup_switch_x64_masm.cmd
              - switch_aarch64_gcc.h
              - switch_alpha_unix.h
              - switch_amd64_unix.h
              - switch_arm32_gcc.h
              - switch_arm32_ios.h
              - switch_arm64_masm.asm
              - switch_arm64_masm.obj
              - switch_arm64_msvc.h
              - switch_csky_gcc.h
              - switch_loongarch64_linux.h
              - switch_m68k_gcc.h
              - switch_mips_unix.h
              - switch_ppc64_aix.h
              - switch_ppc64_linux.h
              - switch_ppc_aix.h
              - switch_ppc_linux.h
              - switch_ppc_macosx.h
              - switch_ppc_unix.h
              - switch_riscv_unix.h
              - switch_s390_unix.h
              - switch_sh_gcc.h
              - switch_sparc_sun_gcc.h
              - switch_x32_unix.h
              - switch_x64_masm.asm
              - switch_x64_masm.obj
              - switch_x64_msvc.h
              - switch_x86_msvc.h
              - switch_x86_unix.h
              - **__pycache__/**
            - **tests/**
              - __init__.py
              - _test_extension.c
              - _test_extension.cpython-310-x86_64-linux-gnu.so
              - _test_extension_cpp.cpp
              - _test_extension_cpp.cpython-310-x86_64-linux-gnu.so
              - fail_clearing_run_switches.py
              - fail_cpp_exception.py
              - fail_initialstub_already_started.py
              - fail_slp_switch.py
              - fail_switch_three_greenlets.py
              - fail_switch_three_greenlets2.py
              - fail_switch_two_greenlets.py
              - leakcheck.py
              - test_contextvars.py
              - test_cpp.py
              - test_extension_interface.py
              - test_gc.py
              - test_generator.py
              - test_generator_nested.py
              - test_greenlet.py
              - test_greenlet_trash.py
              - test_interpreter_shutdown.py
              - test_leaks.py
              - test_stack_saved.py
              - test_throw.py
              - test_tracing.py
              - test_version.py
              - test_weakref.py
              - **__pycache__/**
          - **gunicorn/**
            - __init__.py
            - __main__.py
            - arbiter.py
            - config.py
            - debug.py
            - errors.py
            - glogging.py
            - pidfile.py
            - reloader.py
            - sock.py
            - systemd.py
            - util.py
          - **gunicorn-25.1.0.dist-info/**
            - INSTALLER
            - METADATA
            - RECORD
            - REQUESTED
            - WHEEL
            - entry_points.txt
            - top_level.txt
            - **licenses/**
              - LICENSE
            - **__pycache__/**
            - **app/**
              - __init__.py
              - base.py
              - pasterapp.py
              - wsgiapp.py
              - **__pycache__/**
            - **asgi/**
              - __init__.py
              - lifespan.py
              - message.py
              - protocol.py
              - unreader.py
              - uwsgi.py
              - websocket.py
              - **__pycache__/**
            - **ctl/**
              - __init__.py
              - cli.py
              - client.py
              - handlers.py
              - protocol.py
              - server.py
              - **__pycache__/**
            - **dirty/**
              - __init__.py
              - app.py
              - arbiter.py
              - client.py
              - errors.py
              - protocol.py
              - stash.py
              - tlv.py
              - worker.py
              - **__pycache__/**
            - **http/**
              - __init__.py
              - body.py
              - errors.py
              - message.py
              - parser.py
              - unreader.py
              - wsgi.py
              - **__pycache__/**
            - **http2/**
              - __init__.py
              - async_connection.py
              - connection.py
              - errors.py
              - request.py
              - stream.py
              - **__pycache__/**
            - **instrument/**
              - __init__.py
              - statsd.py
              - **__pycache__/**
            - **uwsgi/**
              - __init__.py
              - errors.py
              - message.py
              - parser.py
              - **__pycache__/**
            - **workers/**
              - __init__.py
              - base.py
              - base_async.py
              - gasgi.py
              - geventlet.py
              - ggevent.py
              - gthread.py
              - gtornado.py
              - sync.py
              - workertmp.py
              - **__pycache__/**
          - **h11/**
            - __init__.py
            - _abnf.py
            - _connection.py
            - _events.py
            - _headers.py
            - _readers.py
            - _receivebuffer.py
            - _state.py
            - _util.py
            - _version.py
            - _writers.py
            - py.typed
          - **h11-0.16.0.dist-info/**
            - INSTALLER
            - METADATA
            - RECORD
            - WHEEL
            - top_level.txt
            - **licenses/**
              - LICENSE.txt
            - **__pycache__/**
          - **itsdangerous/**
            - __init__.py
            - _json.py
            - encoding.py
            - exc.py
            - py.typed
            - serializer.py
            - signer.py
            - timed.py
            - url_safe.py
          - **itsdangerous-2.2.0.dist-info/**
            - INSTALLER
            - LICENSE.txt
            - METADATA
            - RECORD
            - WHEEL
            - **__pycache__/**
          - **jinja2/**
            - __init__.py
            - _identifier.py
            - async_utils.py
            - bccache.py
            - compiler.py
            - constants.py
            - debug.py
            - defaults.py
            - environment.py
            - exceptions.py
            - ext.py
            - filters.py
            - idtracking.py
            - lexer.py
            - loaders.py
            - meta.py
            - nativetypes.py
            - nodes.py
            - optimizer.py
            - parser.py
            - py.typed
            - runtime.py
            - sandbox.py
            - tests.py
            - utils.py
            - visitor.py
          - **jinja2-3.1.6.dist-info/**
            - INSTALLER
            - METADATA
            - RECORD
            - WHEEL
            - entry_points.txt
            - **licenses/**
              - LICENSE.txt
            - **__pycache__/**
          - **jwt/**
            - __init__.py
            - algorithms.py
            - api_jwk.py
            - api_jws.py
            - api_jwt.py
            - exceptions.py
            - help.py
            - jwk_set_cache.py
            - jwks_client.py
            - py.typed
            - types.py
            - utils.py
            - warnings.py
            - **__pycache__/**
          - **markupsafe/**
            - __init__.py
            - _native.py
            - _speedups.c
            - _speedups.cpython-310-x86_64-linux-gnu.so
            - _speedups.pyi
            - py.typed
          - **markupsafe-3.0.3.dist-info/**
            - INSTALLER
            - METADATA
            - RECORD
            - WHEEL
            - top_level.txt
            - **licenses/**
              - LICENSE.txt
            - **__pycache__/**
          - **packaging/**
            - __init__.py
            - _elffile.py
            - _manylinux.py
            - _musllinux.py
            - _parser.py
            - _structures.py
            - _tokenizer.py
            - markers.py
            - metadata.py
            - py.typed
            - pylock.py
            - requirements.py
            - specifiers.py
            - tags.py
            - utils.py
            - version.py
          - **packaging-26.0.dist-info/**
            - INSTALLER
            - METADATA
            - RECORD
            - WHEEL
            - **licenses/**
              - LICENSE
              - LICENSE.APACHE
              - LICENSE.BSD
            - **__pycache__/**
            - **licenses/**
              - __init__.py
              - _spdx.py
              - **__pycache__/**
          - **pip/**
            - __init__.py
            - __main__.py
            - py.typed
          - **pip-22.0.2.dist-info/**
            - INSTALLER
            - LICENSE.txt
            - METADATA
            - RECORD
            - REQUESTED
            - WHEEL
            - entry_points.txt
            - top_level.txt
            - **__pycache__/**
            - **_internal/**
              - __init__.py
              - build_env.py
              - cache.py
              - configuration.py
              - exceptions.py
              - main.py
              - pyproject.py
              - self_outdated_check.py
              - wheel_builder.py
              - **__pycache__/**
              - **cli/**
                - __init__.py
                - autocompletion.py
                - base_command.py
                - cmdoptions.py
                - command_context.py
                - main.py
                - main_parser.py
                - parser.py
                - progress_bars.py
                - req_command.py
                - spinners.py
                - status_codes.py
                - **__pycache__/**
              - **commands/**
                - __init__.py
                - cache.py
                - check.py
                - completion.py
                - configuration.py
                - debug.py
                - download.py
                - freeze.py
                - hash.py
                - help.py
                - index.py
                - install.py
                - list.py
                - search.py
                - show.py
                - uninstall.py
                - wheel.py
                - **__pycache__/**
              - **distributions/**
                - __init__.py
                - base.py
                - installed.py
                - sdist.py
                - wheel.py
                - **__pycache__/**
              - **index/**
                - __init__.py
                - collector.py
                - package_finder.py
                - sources.py
                - **__pycache__/**
              - **locations/**
                - __init__.py
                - _distutils.py
                - _sysconfig.py
                - base.py
                - **__pycache__/**
              - **metadata/**
                - __init__.py
                - base.py
                - pkg_resources.py
                - **__pycache__/**
              - **models/**
                - __init__.py
                - candidate.py
                - direct_url.py
                - format_control.py
                - index.py
                - link.py
                - scheme.py
                - search_scope.py
                - selection_prefs.py
                - target_python.py
                - wheel.py
                - **__pycache__/**
              - **network/**
                - __init__.py
                - auth.py
                - cache.py
                - download.py
                - lazy_wheel.py
                - session.py
                - utils.py
                - xmlrpc.py
                - **__pycache__/**
              - **operations/**
                - __init__.py
                - check.py
                - freeze.py
                - prepare.py
                - **__pycache__/**
                - **build/**
                  - __init__.py
                  - metadata.py
                  - metadata_editable.py
                  - metadata_legacy.py
                  - wheel.py
                  - wheel_editable.py
                  - wheel_legacy.py
                  - **__pycache__/**
                - **install/**
                  - __init__.py
                  - editable_legacy.py
                  - legacy.py
                  - wheel.py
                  - **__pycache__/**
              - **req/**
                - __init__.py
                - constructors.py
                - req_file.py
                - req_install.py
                - req_set.py
                - req_tracker.py
                - req_uninstall.py
                - **__pycache__/**
              - **resolution/**
                - __init__.py
                - base.py
                - **__pycache__/**
                - **legacy/**
                  - __init__.py
                  - resolver.py
                  - **__pycache__/**
                - **resolvelib/**
                  - __init__.py
                  - base.py
                  - candidates.py
                  - factory.py
                  - found_candidates.py
                  - provider.py
                  - reporter.py
                  - requirements.py
                  - resolver.py
                  - **__pycache__/**
              - **utils/**
                - __init__.py
                - _log.py
                - appdirs.py
                - compat.py
                - compatibility_tags.py
                - datetime.py
                - deprecation.py
                - direct_url_helpers.py
                - distutils_args.py
                - egg_link.py
                - encoding.py
                - entrypoints.py
                - filesystem.py
                - filetypes.py
                - glibc.py
                - hashes.py
                - inject_securetransport.py
                - logging.py
                - misc.py
                - models.py
                - packaging.py
                - setuptools_build.py
                - subprocess.py
                - temp_dir.py
                - unpacking.py
                - urls.py
                - virtualenv.py
                - wheel.py
                - **__pycache__/**
              - **vcs/**
                - __init__.py
                - bazaar.py
                - git.py
                - mercurial.py
                - subversion.py
                - versioncontrol.py
                - **__pycache__/**
            - **_vendor/**
              - __init__.py
              - distro.py
              - six.py
              - typing_extensions.py
              - vendor.txt
              - **__pycache__/**
              - **cachecontrol/**
                - __init__.py
                - _cmd.py
                - adapter.py
                - cache.py
                - compat.py
                - controller.py
                - filewrapper.py
                - heuristics.py
                - serialize.py
                - wrapper.py
                - **__pycache__/**
                - **caches/**
                  - __init__.py
                  - file_cache.py
                  - redis_cache.py
                  - **__pycache__/**
              - **certifi/**
                - __init__.py
                - __main__.py
                - cacert.pem
                - core.py
                - **__pycache__/**
              - **chardet/**
                - __init__.py
                - big5freq.py
                - big5prober.py
                - chardistribution.py
                - charsetgroupprober.py
                - charsetprober.py
                - codingstatemachine.py
                - compat.py
                - cp949prober.py
                - enums.py
                - escprober.py
                - escsm.py
                - eucjpprober.py
                - euckrfreq.py
                - euckrprober.py
                - euctwfreq.py
                - euctwprober.py
                - gb2312freq.py
                - gb2312prober.py
                - hebrewprober.py
                - jisfreq.py
                - jpcntx.py
                - langbulgarianmodel.py
                - langgreekmodel.py
                - langhebrewmodel.py
                - langhungarianmodel.py
                - langrussianmodel.py
                - langthaimodel.py
                - langturkishmodel.py
                - latin1prober.py
                - mbcharsetprober.py
                - mbcsgroupprober.py
                - mbcssm.py
                - sbcharsetprober.py
                - sbcsgroupprober.py
                - sjisprober.py
                - universaldetector.py
                - utf8prober.py
                - version.py
                - **__pycache__/**
                - **cli/**
                  - __init__.py
                  - chardetect.py
                  - **__pycache__/**
                - **metadata/**
                  - __init__.py
                  - languages.py
                  - **__pycache__/**
              - **colorama/**
                - __init__.py
                - ansi.py
                - ansitowin32.py
                - initialise.py
                - win32.py
                - winterm.py
                - **__pycache__/**
              - **distlib/**
                - __init__.py
                - compat.py
                - database.py
                - index.py
                - locators.py
                - manifest.py
                - markers.py
                - metadata.py
                - resources.py
                - scripts.py
                - util.py
                - version.py
                - wheel.py
                - **__pycache__/**
              - **html5lib/**
                - __init__.py
                - _ihatexml.py
                - _inputstream.py
                - _tokenizer.py
                - _utils.py
                - constants.py
                - html5parser.py
                - serializer.py
                - **__pycache__/**
                - **_trie/**
                  - __init__.py
                  - _base.py
                  - py.py
                  - **__pycache__/**
                - **filters/**
                  - __init__.py
                  - alphabeticalattributes.py
                  - base.py
                  - inject_meta_charset.py
                  - lint.py
                  - optionaltags.py
                  - sanitizer.py
                  - whitespace.py
                  - **__pycache__/**
                - **treeadapters/**
                  - __init__.py
                  - genshi.py
                  - sax.py
                  - **__pycache__/**
                - **treebuilders/**
                  - __init__.py
                  - base.py
                  - dom.py
                  - etree.py
                  - etree_lxml.py
                  - **__pycache__/**
                - **treewalkers/**
                  - __init__.py
                  - base.py
                  - dom.py
                  - etree.py
                  - etree_lxml.py
                  - genshi.py
                  - **__pycache__/**
              - **idna/**
                - __init__.py
                - codec.py
                - compat.py
                - core.py
                - idnadata.py
                - intranges.py
                - package_data.py
                - uts46data.py
                - **__pycache__/**
              - **msgpack/**
                - __init__.py
                - _version.py
                - exceptions.py
                - ext.py
                - fallback.py
                - **__pycache__/**
              - **packaging/**
                - __about__.py
                - __init__.py
                - _manylinux.py
                - _musllinux.py
                - _structures.py
                - markers.py
                - requirements.py
                - specifiers.py
                - tags.py
                - utils.py
                - version.py
                - **__pycache__/**
              - **pep517/**
                - __init__.py
                - build.py
                - check.py
                - colorlog.py
                - compat.py
                - dirtools.py
                - envbuild.py
                - meta.py
                - wrappers.py
                - **__pycache__/**
                - **in_process/**
                  - __init__.py
                  - _in_process.py
                  - **__pycache__/**
              - **pkg_resources/**
                - __init__.py
                - py31compat.py
                - **__pycache__/**
              - **platformdirs/**
                - __init__.py
                - __main__.py
                - android.py
                - api.py
                - macos.py
                - unix.py
                - version.py
                - windows.py
                - **__pycache__/**
              - **progress/**
                - __init__.py
                - bar.py
                - colors.py
                - counter.py
                - spinner.py
                - **__pycache__/**
              - **pygments/**
                - __init__.py
                - __main__.py
                - cmdline.py
                - console.py
                - filter.py
                - formatter.py
                - lexer.py
                - modeline.py
                - plugin.py
                - regexopt.py
                - scanner.py
                - sphinxext.py
                - style.py
                - token.py
                - unistring.py
                - util.py
                - **__pycache__/**
                - **filters/**
                  - __init__.py
                  - **__pycache__/**
                - **formatters/**
                  - __init__.py
                  - _mapping.py
                  - bbcode.py
                  - groff.py
                  - html.py
                  - img.py
                  - irc.py
                  - latex.py
                  - other.py
                  - pangomarkup.py
                  - rtf.py
                  - svg.py
                  - terminal.py
                  - terminal256.py
                  - **__pycache__/**
                - **lexers/**
                  - __init__.py
                  - _mapping.py
                  - python.py
                  - **__pycache__/**
                - **styles/**
                  - __init__.py
                  - **__pycache__/**
              - **pyparsing/**
                - __init__.py
                - actions.py
                - common.py
                - core.py
                - exceptions.py
                - helpers.py
                - results.py
                - testing.py
                - unicode.py
                - util.py
                - **__pycache__/**
                - **diagram/**
                  - __init__.py
                  - **__pycache__/**
              - **requests/**
                - __init__.py
                - __version__.py
                - _internal_utils.py
                - adapters.py
                - api.py
                - auth.py
                - certs.py
                - compat.py
                - cookies.py
                - exceptions.py
                - help.py
                - hooks.py
                - models.py
                - packages.py
                - sessions.py
                - status_codes.py
                - structures.py
                - utils.py
                - **__pycache__/**
              - **resolvelib/**
                - __init__.py
                - providers.py
                - reporters.py
                - resolvers.py
                - structs.py
                - **__pycache__/**
                - **compat/**
                  - __init__.py
                  - collections_abc.py
                  - **__pycache__/**
              - **rich/**
                - __init__.py
                - __main__.py
                - _cell_widths.py
                - _emoji_codes.py
                - _emoji_replace.py
                - _extension.py
                - _inspect.py
                - _log_render.py
                - _loop.py
                - _lru_cache.py
                - _palettes.py
                - _pick.py
                - _ratio.py
                - _spinners.py
                - _stack.py
                - _timer.py
                - _windows.py
                - _wrap.py
                - abc.py
                - align.py
                - ansi.py
                - bar.py
                - box.py
                - cells.py
                - color.py
                - color_triplet.py
                - columns.py
                - console.py
                - constrain.py
                - containers.py
                - control.py
                - default_styles.py
                - diagnose.py
                - emoji.py
                - errors.py
                - file_proxy.py
                - filesize.py
                - highlighter.py
                - json.py
                - jupyter.py
                - layout.py
                - live.py
                - live_render.py
                - logging.py
                - markup.py
                - measure.py
                - padding.py
                - pager.py
                - palette.py
                - panel.py
                - pretty.py
                - progress.py
                - progress_bar.py
                - prompt.py
                - protocol.py
                - region.py
                - repr.py
                - rule.py
                - scope.py
                - screen.py
                - segment.py
                - spinner.py
                - status.py
                - style.py
                - styled.py
                - syntax.py
                - table.py
                - tabulate.py
                - terminal_theme.py
                - text.py
                - theme.py
                - themes.py
                - traceback.py
                - tree.py
                - **__pycache__/**
              - **tenacity/**
                - __init__.py
                - _asyncio.py
                - _utils.py
                - after.py
                - before.py
                - before_sleep.py
                - nap.py
                - retry.py
                - stop.py
                - tornadoweb.py
                - wait.py
                - **__pycache__/**
              - **tomli/**
                - __init__.py
                - _parser.py
                - _re.py
                - **__pycache__/**
              - **urllib3/**
                - __init__.py
                - _collections.py
                - _version.py
                - connection.py
                - connectionpool.py
                - exceptions.py
                - fields.py
                - filepost.py
                - poolmanager.py
                - request.py
                - response.py
                - **__pycache__/**
                - **contrib/**
                  - __init__.py
                  - _appengine_environ.py
                  - appengine.py
                  - ntlmpool.py
                  - pyopenssl.py
                  - securetransport.py
                  - socks.py
                  - **__pycache__/**
                  - **_securetransport/**
                    - __init__.py
                    - bindings.py
                    - low_level.py
                    - **__pycache__/**
                - **packages/**
                  - __init__.py
                  - six.py
                  - **__pycache__/**
                  - **backports/**
                    - __init__.py
                    - makefile.py
                    - **__pycache__/**
                - **util/**
                  - __init__.py
                  - connection.py
                  - proxy.py
                  - queue.py
                  - request.py
                  - response.py
                  - retry.py
                  - ssl_.py
                  - ssl_match_hostname.py
                  - ssltransport.py
                  - timeout.py
                  - url.py
                  - wait.py
                  - **__pycache__/**
              - **webencodings/**
                - __init__.py
                - labels.py
                - mklabels.py
                - tests.py
                - x_user_defined.py
                - **__pycache__/**
          - **pkg_resources/**
            - __init__.py
            - **__pycache__/**
            - **_vendor/**
              - __init__.py
              - appdirs.py
              - pyparsing.py
              - **__pycache__/**
              - **packaging/**
                - __about__.py
                - __init__.py
                - _manylinux.py
                - _musllinux.py
                - _structures.py
                - markers.py
                - requirements.py
                - specifiers.py
                - tags.py
                - utils.py
                - version.py
                - **__pycache__/**
            - **extern/**
              - __init__.py
              - **__pycache__/**
            - **tests/**
              - **data/**
                - **my-test-package-source/**
                  - setup.py
                  - **__pycache__/**
          - **pyinstaller-6.19.0.dist-info/**
            - INSTALLER
            - METADATA
            - RECORD
            - REQUESTED
            - WHEEL
            - entry_points.txt
            - **licenses/**
              - COPYING.txt
          - **pyinstaller_hooks_contrib-2026.2.dist-info/**
            - INSTALLER
            - METADATA
            - RECORD
            - WHEEL
            - entry_points.txt
            - top_level.txt
            - **licenses/**
              - LICENSE
          - **pyjwt-2.11.0.dist-info/**
            - INSTALLER
            - METADATA
            - RECORD
            - WHEEL
            - top_level.txt
            - **licenses/**
              - AUTHORS.rst
              - LICENSE
          - **pyodbc-5.3.0.dist-info/**
            - INSTALLER
            - METADATA
            - RECORD
            - REQUESTED
            - WHEEL
            - top_level.txt
            - **licenses/**
              - LICENSE.txt
          - **python_engineio-4.13.1.dist-info/**
            - INSTALLER
            - METADATA
            - RECORD
            - WHEEL
            - top_level.txt
            - **licenses/**
              - LICENSE
          - **python_socketio-5.16.1.dist-info/**
            - INSTALLER
            - METADATA
            - RECORD
            - WHEEL
            - top_level.txt
            - **licenses/**
              - LICENSE
          - **setuptools/**
            - __init__.py
            - _deprecation_warning.py
            - _imp.py
            - archive_util.py
            - build_meta.py
            - cli-32.exe
            - cli-64.exe
            - cli-arm64.exe
            - cli.exe
            - config.py
            - dep_util.py
            - depends.py
            - dist.py
            - errors.py
            - extension.py
            - glob.py
            - gui-32.exe
            - gui-64.exe
            - gui-arm64.exe
            - gui.exe
            - installer.py
            - launch.py
            - monkey.py
            - msvc.py
            - namespaces.py
            - package_index.py
            - py34compat.py
            - sandbox.py
            - script (dev).tmpl
            - script.tmpl
            - unicode_utils.py
            - version.py
            - wheel.py
            - windows_support.py
          - **setuptools-59.6.0.dist-info/**
            - INSTALLER
            - LICENSE
            - METADATA
            - RECORD
            - REQUESTED
            - WHEEL
            - entry_points.txt
            - top_level.txt
            - **__pycache__/**
            - **_distutils/**
              - __init__.py
              - _msvccompiler.py
              - archive_util.py
              - bcppcompiler.py
              - ccompiler.py
              - cmd.py
              - config.py
              - core.py
              - cygwinccompiler.py
              - debug.py
              - dep_util.py
              - dir_util.py
              - dist.py
              - errors.py
              - extension.py
              - fancy_getopt.py
              - file_util.py
              - filelist.py
              - log.py
              - msvc9compiler.py
              - msvccompiler.py
              - py35compat.py
              - py38compat.py
              - spawn.py
              - sysconfig.py
              - text_file.py
              - unixccompiler.py
              - util.py
              - version.py
              - versionpredicate.py
              - **__pycache__/**
              - **command/**
                - __init__.py
                - bdist.py
                - bdist_dumb.py
                - bdist_msi.py
                - bdist_rpm.py
                - bdist_wininst.py
                - build.py
                - build_clib.py
                - build_ext.py
                - build_py.py
                - build_scripts.py
                - check.py
                - clean.py
                - config.py
                - install.py
                - install_data.py
                - install_egg_info.py
                - install_headers.py
                - install_lib.py
                - install_scripts.py
                - py37compat.py
                - register.py
                - sdist.py
                - upload.py
                - **__pycache__/**
            - **_vendor/**
              - __init__.py
              - ordered_set.py
              - pyparsing.py
              - **__pycache__/**
              - **more_itertools/**
                - __init__.py
                - more.py
                - recipes.py
                - **__pycache__/**
              - **packaging/**
                - __about__.py
                - __init__.py
                - _manylinux.py
                - _musllinux.py
                - _structures.py
                - markers.py
                - requirements.py
                - specifiers.py
                - tags.py
                - utils.py
                - version.py
                - **__pycache__/**
            - **command/**
              - __init__.py
              - alias.py
              - bdist_egg.py
              - bdist_rpm.py
              - build_clib.py
              - build_ext.py
              - build_py.py
              - develop.py
              - dist_info.py
              - easy_install.py
              - egg_info.py
              - install.py
              - install_egg_info.py
              - install_lib.py
              - install_scripts.py
              - launcher manifest.xml
              - py36compat.py
              - register.py
              - rotate.py
              - saveopts.py
              - sdist.py
              - setopt.py
              - test.py
              - upload.py
              - upload_docs.py
              - **__pycache__/**
            - **extern/**
              - __init__.py
              - **__pycache__/**
          - **simple_websocket/**
            - __init__.py
            - aiows.py
            - asgi.py
            - errors.py
            - ws.py
          - **simple_websocket-1.1.0.dist-info/**
            - INSTALLER
            - LICENSE
            - METADATA
            - RECORD
            - WHEEL
            - top_level.txt
            - **__pycache__/**
          - **socketio/**
            - __init__.py
            - admin.py
            - asgi.py
            - async_admin.py
            - async_aiopika_manager.py
            - async_client.py
            - async_manager.py
            - async_namespace.py
            - async_pubsub_manager.py
            - async_redis_manager.py
            - async_server.py
            - async_simple_client.py
            - base_client.py
            - base_manager.py
            - base_namespace.py
            - base_server.py
            - client.py
            - exceptions.py
            - kafka_manager.py
            - kombu_manager.py
            - manager.py
            - middleware.py
            - msgpack_packet.py
            - namespace.py
            - packet.py
            - pubsub_manager.py
            - redis_manager.py
            - server.py
            - simple_client.py
            - tornado.py
            - zmq_manager.py
            - **__pycache__/**
          - **werkzeug/**
            - __init__.py
            - _internal.py
            - _reloader.py
            - exceptions.py
            - formparser.py
            - http.py
            - local.py
            - py.typed
            - security.py
            - serving.py
            - test.py
            - testapp.py
            - urls.py
            - user_agent.py
            - utils.py
            - wsgi.py
          - **werkzeug-3.1.6.dist-info/**
            - INSTALLER
            - METADATA
            - RECORD
            - WHEEL
            - **licenses/**
              - LICENSE.txt
            - **__pycache__/**
            - **datastructures/**
              - __init__.py
              - accept.py
              - auth.py
              - cache_control.py
              - csp.py
              - etag.py
              - file_storage.py
              - headers.py
              - mixins.py
              - range.py
              - structures.py
              - **__pycache__/**
            - **debug/**
              - __init__.py
              - console.py
              - repr.py
              - tbtools.py
              - **__pycache__/**
              - **shared/**
                - ICON_LICENSE.md
                - console.png
                - debugger.js
                - less.png
                - more.png
                - style.css
            - **middleware/**
              - __init__.py
              - dispatcher.py
              - http_proxy.py
              - lint.py
              - profiler.py
              - proxy_fix.py
              - shared_data.py
              - **__pycache__/**
            - **routing/**
              - __init__.py
              - converters.py
              - exceptions.py
              - map.py
              - matcher.py
              - rules.py
              - **__pycache__/**
            - **sansio/**
              - __init__.py
              - http.py
              - multipart.py
              - request.py
              - response.py
              - utils.py
              - **__pycache__/**
            - **wrappers/**
              - __init__.py
              - request.py
              - response.py
              - **__pycache__/**
          - **wsproto/**
            - __init__.py
            - connection.py
            - events.py
            - extensions.py
            - frame_protocol.py
            - handshake.py
            - py.typed
            - typing.py
            - utilities.py
          - **wsproto-1.3.2.dist-info/**
            - INSTALLER
            - METADATA
            - RECORD
            - WHEEL
            - top_level.txt
            - **licenses/**
              - LICENSE
            - **__pycache__/**

## 2. HTML 템플릿 & 네비게이션 적용 현황

| 파일 | nav.html 포함 | 비고 |
|------|:---:|------|
| admin_login_log.html | ✅ |  |
| admin_user_form.html | ✅ |  |
| admin_users.html | ✅ |  |
| alarms.html | ✅ |  |
| change_password.html | ✅ |  |
| dashboard_preview.html | ❌ | 미리보기 전용 |
| editor.html | ❌ |  |
| executive.html | ✅ |  |
| hospital_detail.html | ✅ |  |
| hospital_view.html | ✅ |  |
| hospitals.html | ✅ |  |
| index.html | ✅ |  |
| index_old.html | ❌ | 구버전 (미사용) |
| isv_detail.html | ✅ |  |
| kiosk_editor.html | ✅ |  |
| kiosk_preview.html | ❌ | 미리보기 전용 |
| login.html | ❌ | 로그인 페이지 (메뉴 불필요) |
| maintenance.html | ✅ |  |
| monitoring.html | ✅ |  |
| monitoring3.html | ✅ |  |
| nav.html | ❌ | 공통 네비게이션 템플릿 |
| setup_monitor.html | ✅ |  |
| ticket_detail.html | ✅ |  |
| ticket_form.html | ✅ |  |
| tickets.html | ✅ |  |
| usage.html | ✅ |  |
| usage_verify.html | ✅ |  |

## 3. Flask 라우트 (app.py)

| 라우트 | 메서드 | 설명 |
|--------|--------|------|
| `/login` | GET, POST | login |
| `/logout` | GET | logout |
| `/` | GET | index |
| `/hospitals` | GET | hospitals |
| `/hospital/<hosp_cd>` | GET | hospital_detail |
| `/admin/users` | GET | admin_users |
| `/admin/user/add` | GET, POST | admin_user_add |
| `/admin/user/edit/<int:user_id>` | GET, POST | admin_user_edit |
| `/admin/user/delete/<int:user_id>` | POST | admin_user_delete |
| `/api/health` | GET | health |
| `/usage` | GET | usage_page |
| `/api/kiosk-usage/receive` | POST | usage_receive |
| `/api/kiosk-usage/dashboard` | GET | usage_dashboard_api |
| `/api/kiosk-usage/daily` | GET | usage_daily_api |
| `/api/kiosk-usage/detail` | GET | usage_detail_api |
| `/api/kiosk-usage/funnel` | GET | usage_funnel_api |
| `/api/kiosk-usage/kiosks` | GET | usage_kiosk_list_api |
| `/usage-verify` | GET | usage_verify |
| `/api/verify/devices` | GET | verify_devices |
| `/api/verify/alarms` | GET | verify_alarms |
| `/api/verify/send-status` | GET | verify_send_status |
| `/setup-monitor` | GET | setup_monitor |
| `/api/setup/start` | POST | api_setup_start |
| `/api/setup/update` | POST | api_setup_update |
| `/api/setup/update-info` | POST | api_setup_update_info |
| `/api/setup/status` | GET | api_setup_status |
| `/api/setup/sessions` | GET | api_setup_sessions |
| `/api/setup/check` | GET | api_setup_check |
| `/api/setup/install-bat` | POST | api_setup_install_bat |
| `/isv/<isv_name>` | GET | isv_detail |
| `/change-password` | GET, POST | change_password |
| `/admin/login-log` | GET | admin_login_log |
| `/editor` | GET | editor |
| `/api/layout` | GET | get_layout |
| `/api/layout` | POST | save_layout |
| `/api/kiosk-monitor` | GET | api_kiosk_monitor |
| `/api/printer-daily/<hosp_cd>/<kiosk_id>` | GET | api_printer_daily |
| `/api/printer-summary` | GET | api_printer_summary |
| `/api/printer-status` | GET | api_printer_status |
| `/api/widget-data/<widget_type>` | GET | widget_data |
| `/dashboard-preview` | GET | dashboard_preview |
| `/alarms` | GET | alarm_list |
| `/alarm/<int:alarm_id>/acknowledge` | POST | acknowledge_alarm |
| `/alarm/<int:alarm_id>/resolve` | POST | resolve_alarm |
| `/tickets` | GET | ticket_list |
| `/ticket/new` | GET,POST | ticket_new |
| `/ticket/<int:ticket_id>` | GET | ticket_detail |
| `/ticket/<int:ticket_id>/comment` | POST | ticket_comment |
| `/ticket/<int:ticket_id>/status` | POST | ticket_status |
| `/api/agent/heartbeat` | POST | agent_heartbeat |
| `/api/agent/status` | GET | agent_status_list |
| `/maintenance` | GET | maintenance |
| `/monitoring` | GET | monitoring |
| `/monitoring3` | GET | monitoring3 |
| `/api/widget-data/alarm_summary` | GET | widget_alarm_summary |
| `/api/widget-data/ticket_summary` | GET | widget_ticket_summary |
| `/api/widget-data/agent_summary` | GET | widget_agent_summary |
| `/api/widget-data/alarm_list` | GET | widget_alarm_list |
| `/api/widget-data/ticket_list` | GET | widget_ticket_list |
| `/api/widget-data/agent_status` | GET | widget_agent_status |
| `/api/widget-data/weekly_trend` | GET | widget_weekly_trend |
| `/api/widgets` | GET | get_widgets |
| `/api/widgets/add` | POST | add_custom_widget |
| `/api/widget-data/monthly_trend` | GET | widget_monthly_trend |
| `/api/widget-data/hourly_usage` | GET | widget_hourly_usage |
| `/api/widget-data/isv_today` | GET | widget_isv_today |
| `/api/widget-data/today_alarm` | GET | widget_today_alarm |
| `/api/widget-data/avg_response` | GET | widget_avg_response |
| `/api/widget-data/month_count` | GET | widget_month_count |
| `/api/widget-data/error_kiosks` | GET | widget_error_kiosks |
| `/api/widget-data/no_heartbeat` | GET | widget_no_heartbeat |
| `/api/widget-data/top10_today` | GET | widget_top10_today |
| `/api/widget-data/daily_trend` | GET | widget_daily_trend |
| `/api/widget-data/daily_hospital_trend` | GET | widget_daily_hospital_trend |
| `/api/widget-data/snapshot_detail` | GET | widget_snapshot_detail |
| `/kiosk-editor` | GET | kiosk_editor |
| `/api/kiosk-components` | GET | get_kiosk_components |
| `/api/kiosk-design/<hosp_cd>` | GET | get_kiosk_design |
| `/api/kiosk-design/<hosp_cd>` | POST | save_kiosk_design |
| `/api/kiosk-design-list/<hosp_cd>` | GET | list_kiosk_designs |
| `/api/kiosk-design-activate/<int:design_id>` | POST | activate_kiosk_design |
| `/api/kiosk-preview/<hosp_cd>` | GET | kiosk_preview |
| `/executive` | GET | executive_dashboard |
| `/api/executive/overview` | GET | api_exec_overview |
| `/api/executive/monthly` | GET | api_exec_monthly |
| `/api/executive/isv-performance` | GET | api_exec_isv |
| `/api/executive/risk-hospitals` | GET | api_exec_risk |
| `/api/executive/top-hospitals` | GET | api_exec_top |
| `/api/executive/scale-distribution` | GET | api_exec_scale |
| `/api/executive/weekday-heatmap` | GET | api_exec_heatmap |
| `/hospital-view` | GET | hospital_view |
| `/api/hospital-view/summary/<hosp_cd>` | GET | api_hosp_summary |
| `/api/hospital-view/daily/<hosp_cd>` | GET | api_hosp_daily |
| `/api/hospital-view/hourly/<hosp_cd>` | GET | api_hosp_hourly |
| `/api/hospital-view/compare/<hosp_cd>` | GET | api_hosp_compare |
| `/api/hospital-list` | GET | api_hospital_list |

## 4. SQLite DB 테이블 (monitor.db)

### alarms (6건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| id | INTEGER | ✅ |  |  |
| hosp_cd | TEXT |  | ✅ |  |
| kiosk_id | TEXT |  |  |  |
| alarm_type | TEXT |  | ✅ |  |
| severity | TEXT |  | ✅ | 'warning' |
| title | TEXT |  | ✅ |  |
| message | TEXT |  |  |  |
| status | TEXT |  |  | 'open' |
| acknowledged_by | TEXT |  |  |  |
| acknowledged_at | TIMESTAMP |  |  |  |
| resolved_by | TEXT |  |  |  |
| resolved_at | TIMESTAMP |  |  |  |
| created_at | TIMESTAMP |  |  | CURRENT_TIMESTAMP |

### daily_summary (8건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| id | INTEGER | ✅ |  |  |
| snap_date | TEXT |  | ✅ |  |
| total_hospitals | INTEGER |  |  | 0 |
| active_hospitals | INTEGER |  |  | 0 |
| total_kiosks | INTEGER |  |  | 0 |
| active_kiosks | INTEGER |  |  | 0 |
| total_count | INTEGER |  |  | 0 |
| created_at | TIMESTAMP |  |  | CURRENT_TIMESTAMP |

### daily_usage_snapshot (612건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| id | INTEGER | ✅ |  |  |
| snap_date | TEXT |  | ✅ |  |
| hosp_cd | TEXT |  | ✅ |  |
| hosp_name | TEXT |  |  |  |
| kiosk_id | TEXT |  | ✅ |  |
| total_count | INTEGER |  |  | 0 |
| isv_name | TEXT |  |  |  |
| created_at | TIMESTAMP |  |  | CURRENT_TIMESTAMP |

### dashboard_layouts (1건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| id | INTEGER | ✅ |  |  |
| name | TEXT |  | ✅ |  |
| user_id | INTEGER |  |  |  |
| role | TEXT |  |  |  |
| layout_json | TEXT |  | ✅ |  |
| is_default | INTEGER |  |  | 0 |
| created_at | TIMESTAMP |  |  | CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP |  |  | CURRENT_TIMESTAMP |

### device_components (0건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| id | INTEGER | ✅ |  |  |
| hosp_cd | TEXT |  | ✅ |  |
| kiosk_id | TEXT |  | ✅ |  |
| component_type | TEXT |  | ✅ |  |
| component_name | TEXT |  |  |  |
| status | TEXT |  |  | 'unknown' |
| detail | TEXT |  |  |  |
| last_checked | TIMESTAMP |  |  |  |
| created_at | TIMESTAMP |  |  | CURRENT_TIMESTAMP |

### heartbeat_log (477건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| id | INTEGER | ✅ |  |  |
| hosp_cd | TEXT |  | ✅ |  |
| kiosk_id | TEXT |  | ✅ |  |
| agent_version | TEXT |  |  |  |
| ip_address | TEXT |  |  |  |
| created_at | TIMESTAMP |  |  | CURRENT_TIMESTAMP |

### kiosk_components (15건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| id | INTEGER | ✅ |  |  |
| comp_key | TEXT |  | ✅ |  |
| name | TEXT |  | ✅ |  |
| category | TEXT |  |  | 'button' |
| icon | TEXT |  |  | '' |
| default_width | INTEGER |  |  | 200 |
| default_height | INTEGER |  |  | 80 |
| default_color | TEXT |  |  | '#2196F3' |
| default_text_color | TEXT |  |  | '#FFFFFF' |
| is_system | INTEGER |  |  | 1 |
| created_at | TIMESTAMP |  |  | CURRENT_TIMESTAMP |

### kiosk_designs (1건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| id | INTEGER | ✅ |  |  |
| hosp_cd | TEXT |  | ✅ |  |
| design_name | TEXT |  | ✅ |  |
| design_json | TEXT |  | ✅ | '[]' |
| screen_width | INTEGER |  |  | 1080 |
| screen_height | INTEGER |  |  | 1920 |
| is_active | INTEGER |  |  | 0 |
| created_by | TEXT |  |  |  |
| created_at | TIMESTAMP |  |  | CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP |  |  | CURRENT_TIMESTAMP |

### kiosk_devices (3건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| id | INTEGER | ✅ |  |  |
| hosp_cd | TEXT |  | ✅ |  |
| kiosk_id | TEXT |  | ✅ |  |
| device_type | TEXT |  | ✅ | 'kiosk' |
| model | TEXT |  |  |  |
| serial_no | TEXT |  |  |  |
| os_version | TEXT |  |  |  |
| ip_local | TEXT |  |  |  |
| ip_public | TEXT |  |  |  |
| teamviewer_id | TEXT |  |  |  |
| install_date | TEXT |  |  |  |
| is_active | INTEGER |  |  | 1 |
| created_at | TIMESTAMP |  |  | CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP |  |  | CURRENT_TIMESTAMP |

### kiosk_status (28건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| id | INTEGER | ✅ |  |  |
| hosp_cd | TEXT |  | ✅ |  |
| kiosk_id | TEXT |  | ✅ |  |
| status | TEXT |  | ✅ | 'unknown' |
| cpu_usage | REAL |  |  |  |
| memory_usage | REAL |  |  |  |
| disk_usage | REAL |  |  |  |
| printer_a4 | TEXT |  |  | 'unknown' |
| printer_thermal | TEXT |  |  | 'unknown' |
| card_reader | TEXT |  |  | 'unknown' |
| barcode_reader | TEXT |  |  | 'unknown' |
| network_speed | REAL |  |  |  |
| emr_connection | TEXT |  |  | 'unknown' |
| agent_version | TEXT |  |  |  |
| last_heartbeat | TIMESTAMP |  |  |  |
| created_at | TIMESTAMP |  |  | CURRENT_TIMESTAMP |
| network_printers | TEXT |  |  | '' |

### login_log (81건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| id | INTEGER | ✅ |  |  |
| username | TEXT |  |  |  |
| success | INTEGER |  |  |  |
| ip_address | TEXT |  |  |  |
| created_at | TIMESTAMP |  |  | CURRENT_TIMESTAMP |

### notification_log (0건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| id | INTEGER | ✅ |  |  |
| alarm_id | INTEGER |  |  |  |
| ticket_id | INTEGER |  |  |  |
| channel | TEXT |  | ✅ |  |
| recipient | TEXT |  | ✅ |  |
| message | TEXT |  |  |  |
| status | TEXT |  |  | 'pending' |
| sent_at | TIMESTAMP |  |  |  |
| created_at | TIMESTAMP |  |  | CURRENT_TIMESTAMP |

### printer_daily_count (0건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| id | INTEGER | ✅ |  |  |
| hosp_cd | TEXT |  | ✅ |  |
| kiosk_id | TEXT |  | ✅ |  |
| printer_name | TEXT |  |  | '' |
| date | TEXT |  | ✅ |  |
| total_count | INTEGER |  |  | 0 |
| daily_count | INTEGER |  |  | 0 |
| toner_pct | INTEGER |  |  | 0 |
| tray1_pct | INTEGER |  |  | 0 |
| tray2_pct | INTEGER |  |  | 0 |
| tray3_pct | INTEGER |  |  | 0 |
| created_at | TIMESTAMP |  |  | CURRENT_TIMESTAMP |

### setup_checklist (81건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| id | INTEGER | ✅ |  |  |
| session_id | INTEGER |  | ✅ |  |
| step | INTEGER |  | ✅ |  |
| category | TEXT |  | ✅ |  |
| item | TEXT |  | ✅ |  |
| check_type | TEXT |  |  | 'auto' |
| status | TEXT |  |  | 'pending' |
| value | TEXT |  |  |  |
| checked_at | DATETIME |  |  |  |

### setup_session (3건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| id | INTEGER | ✅ |  |  |
| kiosk_id | TEXT |  | ✅ |  |
| hosp_cd | TEXT |  |  |  |
| hosp_name | TEXT |  |  |  |
| location | TEXT |  |  |  |
| installer | TEXT |  |  |  |
| status | TEXT |  |  | 'in_progress' |
| started_at | DATETIME |  |  | CURRENT_TIMESTAMP |
| completed_at | DATETIME |  |  |  |

### sqlite_sequence (17건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| name |  |  |  |  |
| seq |  |  |  |  |

### ticket_comments (4건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| id | INTEGER | ✅ |  |  |
| ticket_id | INTEGER |  | ✅ |  |
| author | TEXT |  | ✅ |  |
| comment | TEXT |  | ✅ |  |
| created_at | TIMESTAMP |  |  | CURRENT_TIMESTAMP |

### tickets (1건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| id | INTEGER | ✅ |  |  |
| hosp_cd | TEXT |  | ✅ |  |
| kiosk_id | TEXT |  |  |  |
| alarm_id | INTEGER |  |  |  |
| title | TEXT |  | ✅ |  |
| description | TEXT |  |  |  |
| priority | TEXT |  |  | 'medium' |
| status | TEXT |  |  | 'open' |
| assigned_to | TEXT |  |  |  |
| category | TEXT |  |  |  |
| resolution | TEXT |  |  |  |
| created_by | TEXT |  |  |  |
| created_at | TIMESTAMP |  |  | CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP |  |  | CURRENT_TIMESTAMP |
| closed_at | TIMESTAMP |  |  |  |

### usage_daily_summary (43건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| kiosk_id | TEXT | ✅ | ✅ |  |
| work_date | TEXT | ✅ | ✅ |  |
| first_use_time | TEXT |  |  |  |
| last_use_time | TEXT |  |  |  |
| total_entry | INTEGER |  |  | 0 |
| total_complete | INTEGER |  |  | 0 |
| total_cancel | INTEGER |  |  | 0 |
| complete_rate | REAL |  |  | 0 |
| received_dt | TEXT |  |  |  |

### usage_event_log (18407건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| id | INTEGER | ✅ |  |  |
| kiosk_id | TEXT |  | ✅ |  |
| work_date | TEXT |  | ✅ |  |
| log_dt | TEXT |  |  |  |
| proc_name | TEXT |  |  |  |
| window_title | TEXT |  |  |  |
| class_name | TEXT |  |  |  |
| status | TEXT |  |  |  |
| elapsed_sec | INTEGER |  |  |  |
| received_dt | TEXT |  |  | datetime('now','localtime') |

### usage_kiosk_master (4건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| kiosk_id | TEXT | ✅ |  |  |
| kiosk_name | TEXT |  |  |  |
| location | TEXT |  |  |  |
| hosp_cd | TEXT |  |  |  |
| install_date | TEXT |  |  |  |
| last_received_dt | TEXT |  |  |  |
| reg_dt | TEXT |  |  | datetime('now','localtime') |

### usage_session_log (0건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| id | INTEGER | ✅ |  |  |
| kiosk_id | TEXT |  | ✅ |  |
| work_date | TEXT |  | ✅ |  |
| session_id | TEXT |  |  |  |
| menu_code | TEXT |  |  |  |
| start_dt | TEXT |  |  |  |
| end_dt | TEXT |  |  |  |
| elapsed_sec | INTEGER |  |  |  |
| result | TEXT |  |  |  |
| cancel_step | TEXT |  |  |  |

### usage_step_log (0건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| id | INTEGER | ✅ |  |  |
| kiosk_id | TEXT |  | ✅ |  |
| session_id | TEXT |  |  |  |
| step_order | INTEGER |  |  |  |
| step_name | TEXT |  |  |  |
| start_dt | TEXT |  |  |  |
| end_dt | TEXT |  |  |  |
| elapsed_sec | INTEGER |  |  |  |

### users (7건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| id | INTEGER | ✅ |  |  |
| username | TEXT |  | ✅ |  |
| password_hash | TEXT |  | ✅ |  |
| name | TEXT |  | ✅ |  |
| role | TEXT |  | ✅ | 'hosp_user' |
| org_type | TEXT |  | ✅ | 'hospital' |
| org_code | TEXT |  |  |  |
| phone | TEXT |  |  |  |
| is_active | INTEGER |  |  | 1 |
| created_at | TIMESTAMP |  |  | CURRENT_TIMESTAMP |
| last_login | TIMESTAMP |  |  |  |

### widgets (33건)

| 컬럼명 | 타입 | PK | NOT NULL | 기본값 |
|--------|------|:--:|:--------:|--------|
| id | INTEGER | ✅ |  |  |
| widget_key | TEXT |  | ✅ |  |
| name | TEXT |  | ✅ |  |
| category | TEXT |  | ✅ | 'general' |
| description | TEXT |  |  |  |
| default_width | INTEGER |  |  | 200 |
| default_height | INTEGER |  |  | 120 |
| data_source | TEXT |  |  |  |
| is_system | INTEGER |  |  | 0 |
| is_active | INTEGER |  |  | 1 |
| created_at | TIMESTAMP |  |  | CURRENT_TIMESTAMP |


## 5. 권한별 메뉴 접근 매트릭스

| 메뉴 | 경로 | hq_admin | hosp_admin | isv_admin |
|------|------|:--------:|:----------:|:---------:|
| 대시보드 | `/` | ✅ | ✅ | ✅ |
| 모니터링 | `/monitoring` | ✅ | ✅ | ✅ |
| 병원 | `/hospitals` | ✅ | ❌ | ❌ |
| 행동분석 | `/usage` | ✅ | ✅ | ✅ |
| 유지보수 | `/maintenance` | ✅ | ❌ | ✅ |
| 알람 | `/alarms` | ✅ | ✅ | ✅ |
| 티켓 | `/tickets` | ✅ | ✅ | ✅ |
| 경영진 | `/executive` | ✅ | ❌ | ❌ |
| 병원뷰 | `/hospital-view` | ✅ | ❌ | ❌ |
| 검증 | `/usage-verify` | ✅ | ❌ | ✅ |
| 설치 | `/setup-monitor` | ✅ | ❌ | ✅ |
| 에디터 | `/editor` | ✅ (관리) | ❌ | ❌ |
| 사용자관리 | `/admin/users` | ✅ (관리) | ❌ | ❌ |

## 6. 등록된 사용자

| username | role | org_type | org_code |
|----------|------|----------|----------|
| hosp_002 | hosp_admin | hospital | 002 |
| test | hosp_admin | hospital | HQ |
| admin | hq_admin | hq | HQ |
| dolhan | hq_admin | hq | HQ |
| test1 | hq_admin | hq | HQ |
| isv_jw | isv_admin | isv | JW |
| isv_metro | isv_admin | isv | METRO |