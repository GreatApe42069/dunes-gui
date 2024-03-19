from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QInputDialog, QMessageBox, QLabel, QComboBox, QAction
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
import shutil
import subprocess
import sys
import os
import json

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
        self.setWindowIcon(QIcon('C:/Dunes-GUI/IMG_155.png'))

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
        self.btnSendDunesNoProtocol.clicked.connect(self.sendCombineDunes)

        # Create dropdown for wallet management options
        self.lblWalletOptions = QLabel('Wallet Management Options:')
        self.cmbWalletOptions = QComboBox(self)
        self.cmbWalletOptions.addItem('Existing Wallet')
        self.cmbWalletOptions.addItem('New Wallet')
        self.cmbWalletOptions.addItem('Enter Private Key and Address')

        # Connect dropdown signal
        self.cmbWalletOptions.currentIndexChanged.connect(self.handleWalletOptionChanged)

        # Create menu bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')

        # Add submenu for .env file
        env_action = QAction('&Set .env File', self)
        env_action.triggered.connect(self.setEnvFile)
        fileMenu.addAction(env_action)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.lblWalletOptions)
        layout.addWidget(self.cmbWalletOptions)
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

    def checkExistingWalletFile(self):
        # Define paths
        default_path = 'C:/Doginals-main/Dunes-main/.wallet.json'
        main_wallet_path = 'C:/Dunes-GUI/.wallet.json'

        # Check if .wallet.json file exists in the default path
        if os.path.exists(default_path):
            try:
                # Copy the file from default path to main wallet path
                shutil.copy(default_path, main_wallet_path)

                # Print Wallet Successfully Added if the wallet was found and saved
                print("Wallet copied successfully.")
                QMessageBox.information(self, "Wallet Added", "Wallet Successfully Added")
            except Exception as e:
                # If any error occurs during copying, inform the user
                print(f"Error copying wallet file: {e}")
                QMessageBox.warning(self, "Error", f"Error copying wallet file: {str(e)}")
        else:
            # If no wallet found, inform the user
            print("No existing wallet found in the default path.")
            QMessageBox.warning(self, "Sync Wallet", "No existing wallet found in the default path.")
            self.lblWalletOptions.setText('No Existing Wallet Found. Would you like to Create a New Wallet or Add Private Key and Address?:')
            self.cmbWalletOptions.setEnabled(False)
            self.btnWalletSync.setEnabled(False)

    def handleWalletOptionChanged(self, index):
        if index == 0:  # Existing Wallet
            self.checkExistingWalletFile()
        elif index == 1:  # New Wallet
            self.generateWallet()
        elif index == 2:  # Enter Private Key and Address
            self.promptAndSaveCustomWallet()

    def setEnvFile(self):
        # Get input values for setting .env file
        rpc_user, ok1 = QInputDialog.getText(self, 'Set .env File', 'Enter RPC user:', text=self.getNodeRpcUser())
        rpc_password, ok2 = QInputDialog.getText(self, 'Set .env File', 'Enter RPC password:', text=self.getNodeRpcPassword())
        rpc_port, ok3 = QInputDialog.getText(self, 'Set .env File', 'Enter RPC port:', text=self.getNodeRpcPort())
        testnet, ok4 = QInputDialog.getText(self, 'Set .env File', 'Testnet (true/false):', text=self.getTestnet())
        fee_per_kb, ok5 = QInputDialog.getText(self, 'Set .env File', 'Enter Fee per KB:', text=self.getFeePerKB())
        protocol_identifier, ok6 = QInputDialog.getText(self, 'Set .env File', 'Enter Protocol Identifier:', text=self.getProtocolIdentifier())
        node_rpc_url, ok7 = QInputDialog.getText(self, 'Set .env File', 'Enter Node RPC URL:', text=self.getNodeRpcUrl())
        unsent_api, ok8 = QInputDialog.getText(self, 'Set .env File', 'Enter Unspent API:', text=self.getUnspentAPI())
        ord_url, ok9 = QInputDialog.getText(self, 'Set .env File', 'Enter ORD URL:', text=self.getORD())

        if all([ok1, ok2, ok3, ok4, ok5, ok6, ok7, ok8, ok9]):
            env_content = f"PROTOCOL_IDENTIFIER={protocol_identifier}\n"
            env_content += f"NODE_RPC_URL={node_rpc_url}\n"
            env_content += f"NODE_RPC_USER={rpc_user}\n"
            env_content += f"NODE_RPC_PASS={rpc_password}\n"
            env_content += f"TESTNET={testnet}\n"
            env_content += f"FEE_PER_KB={fee_per_kb}\n"
            env_content += f"UNSPENT_API={unsent_api}\n"
            env_content += f"ORD={ord_url}\n"

            # Write content to .env file
            env_file_path = 'C:/Dunes-GUI/Doginals-main/Dunes-main/.env'
            with open(env_file_path, 'w') as f:
                f.write(env_content)

            QMessageBox.information(self, "Success", ".env file has been updated successfully.")

    # Functions to retrieve default values from existing .env file or set default values
    def getNodeRpcUser(self):
        return 'rpc_user'  # Default value

    def getNodeRpcPassword(self):
        return 'rpc_password'  # Default value

    def getNodeRpcPort(self):
        return '22555'  # Default value

    def getTestnet(self):
        return 'false'  # Default value

    def getFeePerKB(self):
        return '100000000'  # Default value

    def getProtocolIdentifier(self):
        return 'D'  # Default value

    def getNodeRpcUrl(self):
        return 'http://127.0.0.1:22555'  # Default value

    def getUnspentAPI(self):
        return 'https://unspent.dogeord.io/api/v1/address/unspent/'  # Default value

    def getORD(self):
        return 'https://ord.dunesprotocol.com/'  # Default value

    # Functions for wallet operations (generate, sync, etc.)
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
        self.runSubprocess(["node", "C:/Dunes-GUI/Doginals-main/Dunes-main/dunes.js", "wallet", "new"])

    def syncWallet(self):
        # Run subprocess to sync wallet
        self.runSubprocess(["node", "C:/Dunes-GUI/Doginals-main/Dunes-main/dunes.js", "wallet", "sync"])

    def printSafeUtxos(self):
        # Run subprocess to print safe utxos
        self.runSubprocess(["node", "C:/Dunes-GUI/Doginals-main/Dunes-main/dunes.js", "printSafeUtxos"])

    def splitWallet(self):
        # Run subprocess to split wallet
        splits, ok = QInputDialog.getInt(self, 'Split Wallet', 'Enter the number of splits:')
        if ok:
            self.runSubprocess(["node", "C:/Dunes-GUI/Doginals-main/Dunes-main/dunes.js", "wallet", "split", str(splits)])

    def sendFunds(self):
        # Run subprocess to send funds
        address, ok1 = QInputDialog.getText(self, 'Send Funds', 'Enter the recipient address:')
        amount, ok2 = QInputDialog.getText(self, 'Send Funds', 'Enter the amount:')
        if ok1 and ok2:
            self.runSubprocess(["node", "C:/Dunes-GUI/Doginals-main/Dunes-main/dunes.js", "wallet", "send", address, amount])

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
            command = ["node", "C:/Dunes-GUI/Doginals-main/Dunes-main/dunes.js", "deployOpenDune", dune_name, str(blocks), str(limit_per_mint), str(timestamp_deadline), str(decimals), symbol, mint_self, is_open]
            self.runSubprocess(command)

    def mintDune(self):
        # Run subprocess to mint Dune
        # Get input values for minting
        dune_id, ok1 = QInputDialog.getText(self, 'Mint Dune', 'Enter Dune ID:')
        amount, ok2 = QInputDialog.getInt(self, 'Mint Dune', 'Enter amount:')
        to_address, ok3 = QInputDialog.getText(self, 'Mint Dune', 'Enter to address:')
        if ok1 and ok2 and ok3:
            self.runSubprocess(["node", "C:/Dunes-GUI/Doginals-main/Dunes-main/dunes.js", "mintDune", dune_id, str(amount), to_address])

    def massMintDune(self):
        # Run subprocess for mass minting Dune
        # Get input values for mass minting
        dune_name, ok1 = QInputDialog.getText(self, 'Mass Mint Dune', 'Enter Dune name:')
        amount, ok2 = QInputDialog.getInt(self, 'Mass Mint Dune', 'Enter amount:')
        limit_per_mint, ok3 = QInputDialog.getInt(self, 'Mass Mint Dune', 'Enter limit per mint:')
        to_address, ok4 = QInputDialog.getText(self, 'Mass Mint Dune', 'Enter to address:')
        if ok1 and ok2 and ok3 and ok4:
            self.runSubprocess(["node", "C:/Dunes-GUI/Doginals-main/Dunes-main/dunes.js", "massMintDune", dune_name, str(amount), str(limit_per_mint), to_address])

    def printDuneBalance(self):
        # Run subprocess to print Dune balance
        self.runSubprocess(["node", "C:/Dunes-GUI/Doginals-main/Dunes-main/dunes.js", "printDuneBalance"])

    def splitDunes(self):
        # Run subprocess to split Dunes
        # Get input values for splitting Dunes
        to_address, ok1 = QInputDialog.getText(self, 'Split Dunes', 'Enter to address:')
        amount, ok2 = QInputDialog.getInt(self, 'Split Dunes', 'Enter amount:')
        if ok1 and ok2:
            self.runSubprocess(["node", "C:/Dunes-GUI/Doginals-main/Dunes-main/dunes.js", "sendDune", to_address, str(amount)])

    def sendCombineDunes(self):
        # Run subprocess to send or combine Dunes
        # Get input values for sending or combining Dunes
        address, ok1 = QInputDialog.getText(self, 'Send/Combine Dunes', 'Enter address:')
        amount, ok2 = QInputDialog.getInt(self, 'Send/Combine Dunes', 'Enter amount:')
        if ok1 and ok2:
            self.runSubprocess(["node", "C:/Dunes-GUI/Doginals-main/Dunes-main/dunes.js", "send", address, str(amount)])

    def promptAndSaveCustomWallet(self):
        # Prompt user for private key and address
        priv_key, ok1 = QInputDialog.getText(self, 'Enter Private Key and Address', 'Enter Private Key:')
        address, ok2 = QInputDialog.getText(self, 'Enter Private Key and Address', 'Enter Address:')
        
        # If both inputs are provided
        if ok1 and ok2:
            # Create dictionary with provided data
            wallet_data = {
                "privkey": priv_key,
                "address": address,
                "utxos": []
            }
            
            # Save dictionary to .wallet.json file
            wallet_file_path = 'C:/Dunes-GUI/.wallet.json'
            with open(wallet_file_path, 'w') as wallet_file:
                json.dump(wallet_data, wallet_file)
            
            # Inform user that wallet was successfully added
            QMessageBox.information(self, "Wallet Added", "Wallet Successfully Added")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DunesApp()
    ex.show()
    sys.exit(app.exec_())
