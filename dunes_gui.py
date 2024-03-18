from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QInputDialog, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
import subprocess
import sys

class SubprocessThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, command, input_data=""):
        super().__init__()
        self.command = command
        self.input_data = input_data

    def run(self):
        try:
            process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            stdout, stderr = process.communicate(input=self.input_data.encode())
            output = stdout.decode() + stderr.decode()
            self.finished.emit(output)
        except Exception as e:
            self.finished.emit(f"Error running subprocess: {e}")

class DunesApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Dunes Simplified Interface')
        self.setGeometry(100, 100, 800, 600)

        # Set window icon
        self.setWindowIcon(QIcon('C:\\Doginals-main\\Dunes-main\\Dunes GUI\\IMG_155.png'))

        # Initialize thread
        self.thread = None

        self.initUI()

    def initUI(self):
        # Create buttons for each command
        self.btnWalletNew = QPushButton('Generate Wallet', self)
        self.btnWalletSync = QPushButton('Sync Wallet', self)
        self.btnPrintSafeUtxos = QPushButton('Print Safe UTXOs', self)
        self.btnWalletSplit = QPushButton('Split Wallet', self)
        self.btnWalletSend = QPushButton('Send Funds', self)
        self.btnDeployDune = QPushButton('Deploy Dune', self)
        self.btnMintDune = QPushButton('Mint Dune', self)
        self.btnBatchMintDune = QPushButton('Mass Mint Dune', self)
        self.btnPrintDuneBalance = QPushButton('Print Dune Balance', self)
        self.btnSendDuneMulti = QPushButton('Split Send Dunes', self)
        self.btnSendDunesNoProtocol = QPushButton('Send or Combine Dunes', self)

        # Connect buttons to functions
        self.btnWalletNew.clicked.connect(self.generateWallet)
        self.btnWalletSync.clicked.connect(self.syncWallet)
        self.btnPrintSafeUtxos.clicked.connect(self.printSafeUtxos)
        self.btnWalletSplit.clicked.connect(self.splitWallet)
        self.btnWalletSend.clicked.connect(self.sendFunds)
        self.btnDeployDune.clicked.connect(self.deployDune)
        self.btnMintDune.clicked.connect(self.mintDune)
        self.btnBatchMintDune.clicked.connect(self.massMintDune)
        self.btnPrintDuneBalance.clicked.connect(self.printDuneBalance)
        self.btnSendDuneMulti.clicked.connect(self.splitDunes)
        self.btnSendDunesNoProtocol.clicked.connect(self.SendCombineDunes)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.btnWalletNew)
        layout.addWidget(self.btnWalletSync)
        layout.addWidget(self.btnPrintSafeUtxos)
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

    def handleSubprocessFinished(self, output):
        # This slot is called when the subprocess thread finishes
        # Display the output in a message box
        QMessageBox.information(self, "Output", output)

    def generateWallet(self):
        # Run subprocess to generate wallet
        self.runSubprocess(["node", "C:/Doginals-main/Dunes-main/dunes.js", "wallet", "new"])

    def syncWallet(self):
        # Run subprocess to sync wallet
        self.runSubprocess(["node", "C:/Doginals-main/Dunes-main/dunes.js", "wallet", "sync"])

    def printSafeUtxos(self):
        # Run subprocess to print safe utxos
        self.runSubprocess(["node", "C:/Doginals-main/Dunes-main/dunes.js", "printSafeUtxos"])

    def splitWallet(self):
        # Run subprocess to split wallet
        splits, ok = QInputDialog.getInt(self, 'Split Wallet', 'Enter the number of splits:')
        if ok:
            self.runSubprocess(["node", "C:/Doginals-main/Dunes-main/dunes.js", "wallet", "split", str(splits)])

    def sendFunds(self):
        # Run subprocess to send funds
        address, ok1 = QInputDialog.getText(self, 'Send Funds', 'Enter the recipient address:')
        amount, ok2 = QInputDialog.getText(self, 'Send Funds', 'Enter the amount:')
        if ok1 and ok2:
            self.runSubprocess(["node", "C:/Doginals-main/Dunes-main/dunes.js", "wallet", "send", address, amount])

    def deployDune(self):
        # Run subprocess to deploy Dune
        # Get input values for deployment
        dune_name, ok1 = QInputDialog.getText(self, 'Deploy Dune', 'Enter Dune name:')
        blocks, ok2 = QInputDialog.getInt(self, 'Deploy Dune', 'Enter blocks:')
        limit_per_mint, ok3 = QInputDialog.getInt(self, 'Deploy Dune', 'Enter limit per mint:')
        timestamp_deadline, ok4 = QInputDialog.getInt(self, 'Deploy Dune', 'Enter timestamp deadline:')
        decimals, ok5 = QInputDialog.getInt(self, 'Deploy Dune', 'Enter decimals:')
        symbol, ok6 = QInputDialog.getText(self, 'Deploy Dune', 'Enter symbol:')
        mint_self, ok7 = QInputDialog.getText(self, 'Deploy Dune', 'Enter mint self:')
        is_open, ok8 = QInputDialog.getText(self, 'Deploy Dune', 'Enter is open:')
        if ok1 and ok2 and ok3 and ok4 and ok5 and ok6 and ok7 and ok8:
            command = ["node", "C:/Doginals-main/Dunes-main/dunes.js", "deployOpenDune", dune_name, str(blocks), str(limit_per_mint), str(timestamp_deadline), str(decimals), symbol, mint_self, is_open]
            self.runSubprocess(command)

    def mintDune(self):
        # Run subprocess to mint Dune
        # Get input values for minting
        dune_id, ok1 = QInputDialog.getText(self, 'Mint Dune', 'Enter Dune ID:')
        amount, ok2 = QInputDialog.getInt(self, 'Mint Dune', 'Enter amount:')
        to_address, ok3 = QInputDialog.getText(self, 'Mint Dune', 'Enter to address:')
        if ok1 and ok2 and ok3:
            self.runSubprocess(["node", "C:/Doginals-main/Dunes-main/dunes.js", "mintDune", dune_id, str(amount), to_address])

    def massMintDune(self):
        # Run subprocess for mass minting Dune
        # Get input values for mass minting
        dune_id, ok1 = QInputDialog.getText(self, 'Mass Mint Dune', 'Enter Dune ID:')
        amount, ok2 = QInputDialog.getInt(self, 'Mass Mint Dune', 'Enter amount:')
        num_mints, ok3 = QInputDialog.getInt(self, 'Mass Mint Dune', 'Enter number of mints:')
        to_address, ok4 = QInputDialog.getText(self, 'Mass Mint Dune', 'Enter to address:')
        if ok1 and ok2 and ok3 and ok4:
            self.runSubprocess(["node", "C:/Doginals-main/Dunes-main/dunes.js", "massMintDune", dune_id, str(amount), str(num_mints), to_address])

    def printDuneBalance(self):
        # Run subprocess to print Dune balance
        # Still need to finish the necessary parameters for printing balance including catching and displaying the Dunes balance
        self.runSubprocess(["node", "C:/Doginals-main/Dunes-main/dunes.js", "printDunes"])

    def splitDunes(self):
        # Run subprocess to split Dunes
        # Get input values for splitting Dunes
        txhash, ok1 = QInputDialog.getText(self, 'Split Send Dunes', 'Enter txhash:')
        vout, ok2 = QInputDialog.getText(self, 'Split Send Dunes', 'Enter vout:')
        dune, ok3 = QInputDialog.getText(self, 'Split Send Dunes', 'Enter dune:')
        decimals, ok4 = QInputDialog.getInt(self, 'Split Send Dunes', 'Enter decimals:')
        amounts, ok5 = QInputDialog.getText(self, 'Split Send Dunes', 'Enter amounts:')
        addresses, ok6 = QInputDialog.getText(self, 'Split Send Dunes', 'Enter addresses (comma-separated):')
        if ok1 and ok2 and ok3 and ok4 and ok5 and ok6:
            self.runSubprocess(["node", "C:/Doginals-main/Dunes-main/dunes.js", "splitSendDunes", txhash, vout, dune, str(decimals), amounts, addresses])

    def SendCombineDunes(self):
        # Run subprocess to send or combine Dunes
        # Get input values for sending or combining Dunes
        address, ok1 = QInputDialog.getText(self, 'Send or Combine Dunes', 'Enter address:')
        utxo_amount, ok2 = QInputDialog.getInt(self, 'Send or Combine Dunes', 'Enter utxo amount:')
        dune, ok3 = QInputDialog.getText(self, 'Send or Combine Dunes', 'Enter dune:')
        if ok1 and ok2 and ok3:
            self.runSubprocess(["node", "C:/Doginals-main/Dunes-main/dunes.js", "sendCombineDunes", address, str(utxo_amount), dune])

if __name__ == "__main__":
    app = QApplication([])
    window = DunesApp()
    window.show()
    sys.exit(app.exec_())
