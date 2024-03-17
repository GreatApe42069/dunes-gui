from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QInputDialog
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess
import sys

class SubprocessThread(QThread):
    finished = pyqtSignal()

    def __init__(self, command, input_data=""):
        super().__init__()
        self.command = command
        self.input_data = input_data

    def run(self):
        try:
            process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            stdout, stderr = process.communicate(input=self.input_data.encode())
            self.output = stdout.decode() + stderr.decode()
        except Exception as e:
            print(f"Error running subprocess: {e}")
        finally:
            self.finished.emit()

class DunesApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Dunes Simplified Interface')
        self.setGeometry(100, 100, 800, 600)

        # Initialize thread
        self.thread = None

        self.initUI()

    def initUI(self):
        # Create buttons for each command
        self.btnWalletNew = QPushButton('Generate Wallet', self)
        self.btnWalletSync = QPushButton('Sync Wallet', self)
        self.btnWalletSplit = QPushButton('Split Wallet', self)
        self.btnWalletSend = QPushButton('Send Funds', self)
        self.btnDeployDune = QPushButton('Deploy Dune', self)
        self.btnMintDune = QPushButton('Mint Dune', self)
        self.btnBatchMintDune = QPushButton('Mass Mint Dune', self)
        self.btnPrintDuneBalance = QPushButton('Print Dune Balance', self)
        self.btnSendDuneMulti = QPushButton('Split Dunes', self)
        self.btnSendDunesNoProtocol = QPushButton('Combine Dunes', self)

        # Connect buttons to functions
        self.btnWalletNew.clicked.connect(self.generateWallet)
        self.btnWalletSync.clicked.connect(self.syncWallet)
        self.btnWalletSplit.clicked.connect(self.splitWallet)
        self.btnWalletSend.clicked.connect(self.sendFunds)
        self.btnDeployDune.clicked.connect(self.deployDune)
        self.btnMintDune.clicked.connect(self.mintDune)
        self.btnBatchMintDune.clicked.connect(self.massMintDune)
        self.btnPrintDuneBalance.clicked.connect(self.printDuneBalance)
        self.btnSendDuneMulti.clicked.connect(self.splitDunes)
        self.btnSendDunesNoProtocol.clicked.connect(self.combineDunes)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.btnWalletNew)
        layout.addWidget(self.btnWalletSync)
        layout.addWidget(self.btnWalletSplit)
        layout.addWidget(self.btnWalletSend)
        layout.addWidget(self.btnDeployDune)
        layout.addWidget(self.btnMintDune)
        layout.addWidget(self.btnBatchMintDune)
        layout.addWidget(self.btnPrintDuneBalance)
        layout.addWidget(self.btnSendDuneMulti)
        layout.addWidget(self.btnSendDunesNoProtocol)

        # Set the layout for the central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def runSubprocess(self, command, input_data=""):
        # Ensure any existing thread is finished before starting a new one
        if self.thread and self.thread.isRunning():
            self.thread.wait()
            self.thread = None

        self.thread = SubprocessThread(command, input_data)
        self.thread.finished.connect(self.handleSubprocessFinished)
        self.thread.start()

    def handleSubprocessFinished(self):
        # This slot is called when the subprocess thread finishes
        # You can update the UI or perform other tasks here
        # For simplicity, we won't handle specific actions here
        pass

    def generateWallet(self):
        # Run subprocess to generate wallet
        self.runSubprocess(["node", "dunes.js", "wallet", "new"])

    def syncWallet(self):
        # Run subprocess to sync wallet
        self.runSubprocess(["node", "dunes.js", "wallet", "sync"])

    def splitWallet(self):
        # Run subprocess to split wallet
        splits, ok = QInputDialog.getInt(self, 'Split Wallet', 'Enter the number of splits:')
        if ok:
            self.runSubprocess(["node", "dunes.js", "wallet", "split", str(splits)])

    def sendFunds(self):
        # Run subprocess to send funds
        address, ok1 = QInputDialog.getText(self, 'Send Funds', 'Enter the recipient address:')
        amount, ok2 = QInputDialog.getText(self, 'Send Funds', 'Enter the amount:')
        if ok1 and ok2:
            self.runSubprocess(["node", "dunes.js", "wallet", "send", address, amount])

    def deployDune(self):
        # Run subprocess to deploy Dune
        # Need to still add the necessary parameters for deployment
        pass

    def mintDune(self):
        # Run subprocess to mint Dune
        # Need to still add the necessary parameters for deployment
        pass

    def massMintDune(self):
        # Run subprocess for mass minting Dune
        # Need to still add the necessary parameters for deployment
        pass

    def printDuneBalance(self):
        # Run subprocess to print Dune balance
        # Need to still add the necessary parameters for deployment
        pass

    def splitDunes(self):
        # Run subprocess to split Dunes
        # Need to still add the necessary parameters for deployment
        pass

    def combineDunes(self):
        # Run subprocess to combine Dunes
        # Need to still add the necessary parameters for deployment
        pass

if __name__ == "__main__":
    app = QApplication([])
    window = DunesApp()
    window.show()
    sys.exit(app.exec_())
