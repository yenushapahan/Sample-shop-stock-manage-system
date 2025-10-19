#import
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMessageBox,QTableWidgetItem,QComboBox,QLabel,QLineEdit,QDateEdit,QPushButton,QVBoxLayout,QWidget
from PySide6.QtGui import QIcon
import winsound
from resources import JSPYLib
import sys
import datetime
from PySide6.QtGui import QPixmap
import json
from PySide6.QtCharts import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtCore import QDate



class SaleAnalyzer:
    def __init__(self):
        self.loader = QUiLoader()
        self.app = QtWidgets.QApplication(sys.argv)
        #------------------------------------------------------------------------------------------
        #load the style sheet
        with open("./resources/style.qss",'r') as file:
            styleSheet = file.read()
    
        #apply the styleSheet
        self.app.setStyleSheet(styleSheet)

        #call the db handler
        self.mydbfile = JSPYLib.DATABASE()
        
        try:
            #load the login ui
            self.login_window = self.loader.load("Login.ui",None)
            self.login_window.setWindowIcon(QIcon("./resources/icon.png"))

            #load the main window ui
            self.mainWindow = self.loader.load("mainWindow.ui",None)
            self.mainWindow.setWindowIcon(QIcon("./resources/icon.png"))

            #load the worker end ui
            self.sale_window = self.loader.load("./workerEnd/dataEntry.ui",None)
            self.sale_window.setWindowIcon(QIcon("./resources/icon.png"))

            self.saleEdit_window = self.loader.load("./workerEnd/dataEntryEdit.ui",None)
            self.saleEdit_window.setWindowIcon(QIcon("./resources/icon.png"))

            #load the owner end ui
            self.stockEntry_window = self.loader.load("./ownerEnd/stockEntry.ui",None)
            self.stockEntry_window.setWindowIcon(QIcon("./resources/icon.png"))

            self.stockEntryEdit_window = self.loader.load("./ownerEnd/stockEntryEdit.ui",None)
            self.stockEntryEdit_window.setWindowIcon(QIcon("./resources/icon.png"))
            
            #load the invoice file
            self.invoice_window = self.loader.load("./workerEnd/invoice.ui")
            self.invoice_window.setWindowIcon(QIcon("./resources/icon.png"))

            #date time
            self.today = datetime.datetime.today().strftime("%Y/%m/%d")
            self.now = datetime.datetime.now().time().strftime("%H:%M:%S")
        
        except Exception as e:

            self.infoMessage("Ui Load Status",f"There is an Error in Ui Load {e}")
        
        #List Items
        #Shop data list
        self.shopData = []

        #load the inventry
        try:
            self.inventry = self.mydbfile.readData("./databases/inventry")
        
        except:
            self.infoMessage("Database Error!","We cannot load the Inventry Database!")

        try:
            self.stockmoveDb = self.mydbfile.readData("./databases/stockMove")

        except:
            self.infoMessage("Database Error!","We cannot load the Stock Move Database!")
        
        #load the Sale Entry Items
        try:
            #add date to date label
            self.sale_window.date_lable.setText(str(self.today))

            self.productName_SE = self.sale_window.productName_comboBox
            self.productSize_SE = self.sale_window.size_comboBox
            self.productPrice_SE = self.sale_window.price_lineEdit
            self.productCount_SE = self.sale_window.itemCount_spinBox

            self.addBtn_SE = self.sale_window.add_btn
            self.saleItemTable_SE = self.sale_window.item_table
            self.totalOfItems = self.sale_window.totalOfItems_lineEdit
            self.clearBtn_SE = self.sale_window.clearBtn
            self.giveChangeBtn_SE = self.sale_window.giveaChangeBtn
        
        except Exception as e:
            self.infoMessage("Ui Load Status",f"There is an Error in Ui Load {e}")
        
        #load the Sale Entry Edit Items
        try:
            self.productName_SE_Edit = self.saleEdit_window.productName_STM_Edit_lineEdit
            self.productPrice_SE_Edit = self.saleEdit_window.price_STM_Edit_lineEdit 
            self.productSize_SE_Edit = self.saleEdit_window.size_STM_Edit_comboBox
            self.productCount_SE_Edit = self.saleEdit_window.itemCount_STM_Edit_spinBox

            self.saleEditSaveBtn = self.saleEdit_window.save_btn 

        except Exception as e:
            self.infoMessage("Ui Load Status",f"There is an Error in Ui Load {e}")
        
        #load the invoice items
        try:
            self.invoice_window.date.setText(str(self.today))
            
            self.invoice_table = self.invoice_window.invoiceItemsTable
            self.totalAmount = self.invoice_window.totalAmount
            self.InvoiceNumber = self.invoice_window.InvoiceNumber

        except Exception as e:
            self.infoMessage("Ui Load Status",f"There is an Error in Ui Load {e}")

        #load the Stock Entry
        try:
            self.stockEntry_window.date_lable.setText(str(self.today))

            self.productName_In = self.stockEntry_window.productName_SM_lineEdit
            self.productPrice_In = self.stockEntry_window.price_SM_lineEdit
            self.productCustumer_In = self.stockEntry_window.custumer_SM_lineEdit
            self.productCategory_In = self.stockEntry_window.size_SM_comboBox
            self.productCount_In = self.stockEntry_window.itemCount_SM_spinBox

            self.addBtn_In_btn = self.stockEntry_window.add_SM_btn

            self.inventryTable = self.stockEntry_window.inventryTable
            self.stockMoveTable = self.stockEntry_window.stockMoveTable
            
        except Exception as e:
            self.infoMessage("Ui Load Status",f"There is an Error in Ui Load {e}")

        #load the Main window items
        try:
            #date edit items
            self.saleBeginDate = self.mainWindow.beginSaleDateEdit
            self.saleEndDate = self.mainWindow.endSaleDateEdit

            #main lable items
            self.totalItemsCount = self.mainWindow.totalItemsCount
            self.totalSaleItemCount = self.mainWindow.totalSaleCount
            self.availableCategoriesCount = self.mainWindow.availableCategoriesCount
            self.totalBuyingCount = self.mainWindow.totalBuyingCount

        except:
            self.infoMessage("Ui Load Status",f"There is an Error in Ui Load {e}")
        #show the login window
        self.login_window.show()

        #button actions -------------------------------------------------------------------------
        #login btn
        loginBtn = self.login_window.loginBtn
        loginBtn.clicked.connect(self.login)

        #add Button
        self.addBtn_SE.clicked.connect(self.addProduct)

        #save Button
        self.saleEditSaveBtn.clicked.connect(self.saveEditedSaleData)

        #clear Buttnon
        self.clearBtn_SE.clicked.connect(self.clearContent)

        #give a change Button
        self.giveChangeBtn_SE.clicked.connect(self.giveaChange)

        #add inventry Button
        self.addBtn_In_btn.clicked.connect(self.addDataToStockMove)

        #work with main window
        try:
            self.mainWindow.actionSale_Entry.triggered.connect(self.saleEntry)
        
        except:
            self.infoMessage("Ui Item Load Status","There is and Error with Sale Entry Function!")

        try :
            self.mainWindow.action_Stock_Entry.triggered.connect(self.loadStockMoveEntry)

        except:
            self.infoMessage("Ui Item Load Status","There is and Error with Stock Move Entry Function!")

        #call the sales bar chart
        self.saleBeginDate.dateChanged.connect(self.loadTheSaleReportBarChart)

        self.saleEndDate.dateChanged.connect(self.loadTheSaleReportBarChart)

        #load the total of item count
        self.loadTheTotalItemCountOfBussines()

        #load the total of the sold items Count
        self.loadTheTotalItemCountOfSold()

        #load the avilable categories of store
        self.loadTheCountOfAvaiableCategories()

        self.loadTheSaleDates()

        #---------------------------------------------------------------------------
        self.app.exec()
        pass

    #info-message-function
    def infoMessage(self,infoTitle,message):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(infoTitle)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(message)
        msgBox.setWindowIcon(QIcon("./resources/icon.png"))
        msgBox.exec()
        pass

    def login(self):
        username = self.login_window.username
        password = self.login_window.password
        
        if not username.text():
            self.infoMessage("Login Status",'Username Field Cannot be empty!')
            username.setFocus()
            return
        
        if not password.text():
            self.infoMessage("Login Status","Password Field Cannot be empty!")
            password.setFocus()
            return
        
        #check the login
        if (
            (self.mydbfile.searchData("./databases/loginDetails","username",username.text())) and
            (self.mydbfile.searchData("./databases/loginDetails","password",password.text()))
        ):
            
            self.infoMessage("Login Status","You have login successfully!")

            #close the login window
            self.login_window.close()

            #open the main window
            self.mainWindow.show()
        
        else:
            self.infoMessage("Login Status","Your username or Password is wrong!")

            #clear the fields
            username.setText("")
            password.setText("")

            username.setFocus()

            return
    
    #-----------------------------------------------------------------------------------------------
    #Sale Entry Functions
    #sale Entry
    def saleEntry(self):
        #show the Ui
        self.sale_window.show()

        #Load the inventry items
        self.loadTheInventryItems()

    #load the inventry Items
    def loadTheInventryItems(self):
        try:
            self.itemNames = self.mydbfile.findUniqItems("./databases/inventry","productName")
            self.itemNames = [i.upper() for i in self.itemNames]
            self.itemNames = sorted(self.itemNames)

            self.productName_SE.clear()
            self.productSize_SE.clear()

            self.productName_SE.addItem("")
            self.productSize_SE.addItem("")

            self.productName_SE.addItems(self.itemNames)

            #load the Sizes
            def loadSizes():
                self.productSize_SE.clear()
                self.productSize_SE.addItem("")

                for product in self.inventry:
                    if product["productName"].lower() == self.productName_SE.currentText().lower():
                        self.productSize_SE.addItem(product["productCategory"].upper())
            
            #when select the product Name
            self.productName_SE.currentTextChanged.connect(loadSizes)

            #load the prices
            def loadPrices():
                for product in self.inventry:
                    if (
                        (product["productName"].lower() == self.productName_SE.currentText().lower()) and
                        (product["productCategory"].lower() == self.productSize_SE.currentText().lower())
                        ):

                        self.productPrice_SE.setText(str(product["productPrice"]))
                pass

            #when select the product Name and Size
            self.productSize_SE.currentTextChanged.connect(loadPrices)
            
        
        except:
            self.infoMessage("Error in Load Items!","Cannot load the Product Names,Categories and Prices due to Inventry Db error!")
    
    #check product Amount custumer can buy
    def checkProductAmount(self,productDetails):
        #print(productDetails)
        #call the inventry db
        inventry = self.mydbfile.searchData(
            fileName="./databases/inventry",
            keyOfDict="productName",
            valueOfDict=productDetails[0].lower()
        )

        #print(inventry)

        results = [item for item in inventry if(item["productCategory"].lower() == productDetails[1].lower())]

        #print(results)

        if results:
            if results[0]["productCount"] <= productDetails[3]:
                self.infoMessage("Inventry Storage Capacity",f"You Can Only Buy {results[0]["productCount"]} items only.")
                self.productCount_SE.setValue(int(results[0]["productCount"]))
                self.productCount_SE_Edit.setValue(int(results[0]["productCount"]))

                #results[0]["productCount"] = results[0]["productCount"] - productDetails[3] should equal to 0
                results[0]["productCount"] = 0

                #update the inventry
                self.mydbfile.updateData("./databases/inventry",results[0]["productId"],results[0])
                return 
            
            else:
                results[0]["productCount"] = results[0]["productCount"] - productDetails[3] 

                #update the inventry
                self.mydbfile.updateData("./databases/inventry",results[0]["productId"],results[0])
        

    #add products
    def addProduct(self):
        #presence check
        if not self.productName_SE.currentText():
            self.infoMessage("Data Presence Check","Product Name Field Cannot be Empty!")
            self.productName_SE.setFocus()
            return
        
        if not self.productSize_SE.currentText():
            self.infoMessage("Data Presence Check","Product Size Field Cannot be Empty!")
            self.productSize_SE.setFocus()
            return
        
        if not self.productPrice_SE.text():
            self.infoMessage("Data Presence Check","Product Price Field Cannot be Empty!")
            self.productPrice_SE.setFocus()
            return
        
        if not self.productCount_SE.text():
            self.infoMessage("Data Presence Check","Product Count Field Cannot be Empty!")
            self.productCount_SE.setFocus()
            return
        
        #check the product Amount
        if self.productCount_SE.text():
            self.checkProductAmount([
                self.productName_SE.currentText(),
                self.productSize_SE.currentText(),
                self.productPrice_SE.text(),
                int(self.productCount_SE.text())
                ])

        #product description
        self.productSaleDataSet = {
            "shopId":len(self.shopData),
            "date":self.today,
            "now":self.now,
            "productName":self.productName_SE.currentText(),
            "productSize":self.productSize_SE.currentText(),
            "productPrice":self.productPrice_SE.text(),
            "productCount":self.productCount_SE.text(),
            "total":float(self.productPrice_SE.text()) * int(self.productCount_SE.text())
        }

        #add product Sale to the Shopdata List
        self.shopData.append(self.productSaleDataSet)

        #add product data to product description table
        self.productShowTable()
    
    #edit sale data function
    def editSaleData(self,shopdataSet):
        #show the edit data ui
        self.saleEdit_window.show()

        #print(shopdataSet)

        #load the shopdata to shop dataedit window
        self.productName_SE_Edit.setText(shopdataSet["productName"])
        self.productPrice_SE_Edit.setText(shopdataSet["productPrice"])
        self.productSize_SE_Edit.setText(shopdataSet["productSize"])
        self.productCount_SE_Edit.setValue(int(shopdataSet["productCount"]))

        #re apply the table
        self.productShowTable()

    #save btn
    def saveEditedSaleData(self):
        #check the inventry
        self.checkProductAmount([
            self.productName_SE_Edit.text(),
            self.productSize_SE_Edit.text(),
            self.productPrice_SE_Edit.text(),
            int(self.productCount_SE_Edit.text())
        ])

        #saved dataset
        try:
            self.editedDataset = {
                "shopId":len(self.shopData),
                "date":self.today,
                "now":self.now,
                "productName":self.productName_SE_Edit.text(),
                "productPrice":self.productPrice_SE_Edit.text(),
                "productSize":self.productSize_SE_Edit.text(),
                "productCount":self.productCount_SE_Edit.value(),
                "total":float(self.productPrice_SE_Edit.text()) * int(self.productCount_SE_Edit.value())
            }
        
        except Exception as e:
            self.infoMessage("Data Load Status",f"There is a Error in load data to edited {e}")

        #add them into shopdata list
        self.shopData.append(self.editedDataset)

        #close the sale edit window
        self.saleEdit_window.close()

        #re apply the table
        self.productShowTable()

    #add data to product table
    def productShowTable(self):
        self.total = 0

        #clear the table items
        self.saleItemTable_SE.clearContents()
        self.saleItemTable_SE.setRowCount(0)

        for self.item in self.shopData:
            rowPosition = self.saleItemTable_SE.rowCount()

            self.saleItemTable_SE.insertRow(rowPosition)

            self.saleItemTable_SE.setItem(rowPosition,0,QTableWidgetItem(str(self.item["productName"])))
            self.saleItemTable_SE.setItem(rowPosition,1,QTableWidgetItem(str(self.item["productSize"])))
            self.saleItemTable_SE.setItem(rowPosition,2,QTableWidgetItem(str(self.item["productPrice"])))
            self.saleItemTable_SE.setItem(rowPosition,3,QTableWidgetItem(str(self.item["productCount"])))
            self.saleItemTable_SE.setItem(rowPosition,4,QTableWidgetItem(str(self.item["total"])))

            #define a combo box
            actionCombo = QComboBox()
            actionCombo.addItems(["","Edit","Delete"])

            def handleAction(index,rowIndex):
                if actionCombo.itemText(index) == "Edit":
                    #call the sale edit function
                    shopdataSet = self.shopData.pop(rowIndex)

                    self.editSaleData(shopdataSet)

                    #show the Ui
                    self.saleEdit_window.show()

                    #set the current text
                    actionCombo.setCurrentText("")

                    #recall the table
                    self.productShowTable()
                    pass

                if actionCombo.itemText(index) == "Delete":
                    userResponse = QMessageBox.question(
                        self.sale_window,
                        "Confirmation For Delete",
                        "Are you sure you want to delete this item?",
                        QMessageBox.Yes | QMessageBox.No
                    )

                    if userResponse == QMessageBox.Yes:
                        #delete the data row
                        self.shopData.pop(rowIndex)

                        #re call the table
                        self.productShowTable()

            #connect the action combo signal
            actionCombo.currentIndexChanged.connect(lambda index,rowIndex = rowPosition: handleAction(index,rowIndex))
            
            #add action combo to the table
            self.saleItemTable_SE.setCellWidget(rowPosition,5,actionCombo)

            #increament the total
            self.total = self.total + float(self.item["total"])
        
        #set the total amount
        self.totalOfItems.setText(str(self.total))

        #clear the fields
        self.productName_SE.setCurrentText("")
        self.productSize_SE.setCurrentText("")
        self.productPrice_SE.setText("")
        self.productCount_SE.setValue(0)

        self.productName_SE.setFocus()

        pass
    
    #clear the content
    def clearContent(self):
        #clear the table
        self.saleItemTable_SE.clearContents()
        self.saleItemTable_SE.setRowCount(0)

        #clear the shopdata list
        self.shopData = []

        #set focus the product Name
        self.productName_SE.setFocus()

        #clear the total
        self.total = 0

        #clear the fields items 
        self.productName_SE.setCurrentText("")
        self.productSize_SE.setCurrentText("")
        self.productPrice_SE.setText("")
        self.productCount_SE.setValue(0)
        self.totalOfItems.setText("")

        self.productName_SE.setFocus()

        #re apply the table
        self.productShowTable()
        pass

    #give a change Button
    def giveaChange(self):
        self.total  # Declare total as global to access it
        class InputDialog(QtWidgets.QDialog):
            def __init__(self, title, label_text):
                super().__init__()
                self.setWindowTitle(title)

                screen_geometry = QtWidgets.QApplication.primaryScreen().geometry()
                dialog_width = 300
                dialog_height = 150
                x = (screen_geometry.width() - dialog_width) // 2
                y = (screen_geometry.height() - dialog_height) // 2
                self.setGeometry(x, y, dialog_width, dialog_height)

                # UI Elements
                self.label = QLabel(label_text)
                self.entry = QLineEdit()
                self.button = QPushButton("OK")

                # Layout
                layout = QVBoxLayout()
                layout.addWidget(self.label)
                layout.addWidget(self.entry)
                layout.addWidget(self.button)
                self.setLayout(layout)

                # Connect button to close dialog
                self.button.clicked.connect(self.accept)

            def get_text(self):
                return self.entry.text()

        # Create and show the dialog
        dialog = InputDialog("Recieve", "Recieve")
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            try:
                chargeFromCustumer = float(dialog.get_text())
                if chargeFromCustumer >= self.total:
                    change = chargeFromCustumer - self.total
                    self.infoMessage( "Change",f"Change: Rs. {change}/=")
                else:
                    self.infoMessage("Input Error","Received amount is less than the total.")
            except ValueError:
                self.infoMessage("Input Error","Received amount is less than the total.")

                if chargeFromCustumer >= self.total:
                    change = chargeFromCustumer - self.total
                    self.infoMessage("Change ",f"Change:Rs. {change}/=")

        #call the invoice function
        self.invoice()

        pass

    def invoice(self):
        #show the window
        self.invoice_window.show()

        #load the items to invoce window  items
        #clear the table
        self.invoice_table.clearContents()
        self.invoice_table.setRowCount(0)

        totalOfProducts = 0

        for self.product in self.shopData:
            rowPosition = self.invoice_table.rowCount()

            self.invoice_table.insertRow(rowPosition)

            self.invoice_table.setItem(rowPosition,0,QTableWidgetItem(str(f"{self.product["productSize"]} Size {self.item["productName"]}")))
            self.invoice_table.setItem(rowPosition,1,QTableWidgetItem(str(self.product["productPrice"])))
            self.invoice_table.setItem(rowPosition,2,QTableWidgetItem(str(self.product["productCount"])))
            self.invoice_table.setItem(rowPosition,3,QTableWidgetItem(str(self.product["total"])))

            totalOfProducts = totalOfProducts + self.product["total"]
        #assign total
        self.totalAmount.setText(f"{totalOfProducts}/=")

        try:
            self.mydbfile.insertData("./databases/shopdata",self.shopData)

            self.shopDataToStockMove(self.shopData)
            
        except Exception as e:
            self.infoMessage("Data Base Operation Status!",f"We cannot complete this action, {e}")

        #getting invoice number
        invoiceNumber = self.mydbfile.gettingIndex("./databases/shopdata")

        # Connect Enter key press to printTheInvoice
        self.printTheInvoice(self.invoice_window,f"./invoices/{invoiceNumber}_invoice.png")

        #call the inventry Table
        self.showInventryTable()

        #call the Stock Move show table fuction
        self.showStockMoveTable()

        #-------------------------------------------------------------------------------------------
        #call the main window widgets

        #load the total of item count
        self.loadTheTotalItemCountOfBussines()

        #load the total of the sold items Count
        self.loadTheTotalItemCountOfSold()

        #load the avilable categories of store
        self.loadTheCountOfAvaiableCategories()

        #call the sale report
        self.loadTheSaleReportBarChart()

    #print the invoice
    def printTheInvoice(self,widget: QWidget, filename: str):
        pixmap = QPixmap(widget.size())
        widget.render(pixmap)
        pixmap.save(filename, "PNG")

        pass

    #-----------------------------------------------------------------------------------------------------
    #stock Entry Ui Fucntions
    def loadStockMoveEntry(self):
        #load the Ui
        self.stockEntry_window.show()

        #show the inventry Table
        self.showInventryTable()

        #call the Stock Move show table fuction
        self.showStockMoveTable()


    #show Inventry Table
    def showInventryTable(self):
        #load the inventry Data Base
        self.inventryDb = self.mydbfile.readData("./databases/inventry")

        #clear the table
        self.inventryTable.clearContents()
        self.inventryTable.setRowCount(0)

        for inventryitem in self.inventryDb:
            rowPosition = self.inventryTable.rowCount()

            self.inventryTable.insertRow(rowPosition)

            self.inventryTable.setItem(rowPosition,0,QTableWidgetItem(str(inventryitem["productName"])))
            self.inventryTable.setItem(rowPosition,1,QTableWidgetItem(str(inventryitem["productCategory"])))
            self.inventryTable.setItem(rowPosition,2,QTableWidgetItem(str(inventryitem["productPrice"])))
            self.inventryTable.setItem(rowPosition,3,QTableWidgetItem(str(inventryitem["productCount"])))
        


    #add data to stock move data base from shopdata data base
    def shopDataToStockMove(self,shopDataset):
        #add data to stock move
        for item in shopDataset:
            stockMoveDataset = {
                "STM_Number":self.mydbfile.gettingIndex("./databases/stockMove"),
                "date":self.today,
                "time":self.now,
                "productName":item["productName"],
                "productSize":item["productSize"],
                "productPrice":item["productPrice"],
                "productCount":item["productCount"],
                "productCustumer":"-",
                "productMove":"out"
            }

            self.mydbfile.insertData2('./databases/stockMove',stockMoveDataset)

            saleDataset = {
                "shopId": 19, 
                "date": self.today, 
                "now": self.now, 
                "productName": item["productName"], 
                "productSize": item["productSize"], 
                "productPrice": item["productPrice"], 
                "productCount": item["productCount"], 
                "total": float(item["productPrice"]) * int(item["productCount"]) 
            }

            self.mydbfile.insertData2("./databases/sale",saleDataset)
        
        #call the Stock Move show table fuction
        self.showStockMoveTable()

        
        pass
    
    #add data to stock move table
    def addDataToStockMove(self):
        if not self.productName_In.text():
            self.infoMessage("Precense Check","Product Name Field Cannot be Empty!")
            self.productName_In.setFocus()
            return
        
        if not self.productPrice_In.text():
            self.infoMessage("Presence Check","Product Price Field Cannot be Empty!")
            self.productPrice_In.setFocus()
            return
        
        if not self.productCategory_In.currentText():
            self.infoMessage("Presence Check","Product Category Field Cannot be Empty!")
            self.productCategory_In.setFocus()
            return
        
        stockMoveDataset = {
            "STM_Number": self.mydbfile.gettingIndex("./databases/stockMove"),
            "date": self.today,
            "time": self.now,
            "productName": self.productName_In.text(),
            "productSize": self.productCategory_In.currentText(),
            "productPrice":self.productPrice_In.text(),
            "productCount":self.productCount_In.text(),
            "productCustumer": self.productCustumer_In.text(),
            "productMove": "in"
        }

        #insert the data set
        self.mydbfile.insertData2("./databases/stockMove",stockMoveDataset)

        #call the stockMoveTable show function
        self.showStockMoveTable()

        #update the inventry
        self.updateInventry(stockMoveDataset)

        #append the data into inventry
        self.inventryDb.append(stockMoveDataset)

        #clear the contents
        self.productName_In.setText("")
        self.productPrice_In.setText("")
        self.productCategory_In.setCurrentText("")
        self.productCustumer_In.setText("")
        self.productCount_In.setValue(0)

        self.productName_In.setFocus()

        #-------------------------------------------------------------------------------------------
        #call the main window widgets
        
        #load the total of item count
        self.loadTheTotalItemCountOfBussines()

        #load the total of the sold items Count
        self.loadTheTotalItemCountOfSold()

        #load the avilable categories of store
        self.loadTheCountOfAvaiableCategories()

    #update the inventry accordinng to stock Move Update
    def updateInventry(self, stockMoveDataset):
        try:
            # Step 1: Search by productName
            inventry = self.mydbfile.searchData(
                "./databases/inventry",
                "productName",
                stockMoveDataset["productName"].lower()
            )
        except Exception as e:
            self.infoMessage("Database Action", f"This action cannot be fulfilled! {e}")
            return

        # Step 2: Define common inventory entry from stockMoveDataset
        newEntry = {
            "productId": self.mydbfile.gettingIndex("./databases/inventry"),
            "productName": stockMoveDataset["productName"],
            "productPrice": stockMoveDataset["productPrice"],
            "productCategory": stockMoveDataset["productSize"],  # Assuming productSize is category
            "productCount": int(stockMoveDataset["productCount"])
        }

        # Step 3: If no productName match, insert new
        if not inventry:
            try:
                self.mydbfile.insertData2("./databases/inventry", newEntry)
            except Exception as e:
                self.infoMessage("Database Action", f"Insert failed! {e}")
            finally:
                self.showInventryTable()
                self.showStockMoveTable()
            return

        try:
            # Step 4: Filter by matching category
            matched = [item for item in inventry if item["productCategory"] == stockMoveDataset["productSize"]]

            if not matched:
                # No exact match, insert new record
                self.mydbfile.insertData2("./databases/inventry", newEntry)
            else:
                result = matched[0]  # Use first match
                updatedCount = int(result["productCount"]) + int(stockMoveDataset["productCount"])

                # Update existing record with new count
                result["productCount"] = updatedCount

                self.mydbfile.updateData(
                    "./databases/inventry",
                    result["productId"],
                    result
                )

        except Exception as e:
            self.infoMessage("Database Action", f"Update failed! {e}")
        finally:
            self.showInventryTable()
            self.showStockMoveTable()


    #add data to stock Move Table
    def showStockMoveTable(self):

        self.stockMoveTable.clearContents()
        self.stockMoveTable.setRowCount(0)

        for stock in self.stockmoveDb:
            rowPosition = self.stockMoveTable.rowCount()

            self.stockMoveTable.insertRow(rowPosition)

            self.stockMoveTable.setItem(rowPosition,0,QTableWidgetItem(str(stock["date"])))
            self.stockMoveTable.setItem(rowPosition,1,QTableWidgetItem(str(stock["productName"])))
            self.stockMoveTable.setItem(rowPosition,2,QTableWidgetItem(str(stock["productSize"])))
            self.stockMoveTable.setItem(rowPosition,3,QTableWidgetItem(str(stock["productPrice"])))
            self.stockMoveTable.setItem(rowPosition,4,QTableWidgetItem(str(stock["productCount"])))
            self.stockMoveTable.setItem(rowPosition,5,QTableWidgetItem(str(stock["productCustumer"])))

            #define a combo box
            actionCombo = QComboBox()
            actionCombo.addItems(["","Edit","Delete"])

            def handleAction(index,rowIndex):
                if actionCombo.itemText(index) == "Edit":
                    #call the sale edit function
                    stockMovedataSet = self.stockmoveDb.pop(rowIndex)

                    self.editSaleData(stockMovedataSet)

                    #show the Ui
                    self.stockEntryEdit_window.show()

                    #set the current text
                    actionCombo.setCurrentText("")

                    #recall the table
                    self.showStockMoveTable()

                    #recall the table
                    self.showInventryTable()
                    pass

                if actionCombo.itemText(index) == "Delete":
                    userResponse = QMessageBox.question(
                        self.stockEntry_window,
                        "Confirmation For Delete",
                        "Are you sure you want to delete this item?",
                        QMessageBox.Yes | QMessageBox.No
                    )

                    if userResponse == QMessageBox.Yes:
                        #delete the data row
                        self.stockmoveDb.pop(rowIndex)

                        #recall the table
                        self.showStockMoveTable()

                        #recall the table
                        self.showInventryTable()

            #connect the action combo signal
            actionCombo.currentIndexChanged.connect(lambda index,rowIndex = rowPosition: handleAction(index,rowIndex))
            
            #add action combo to the table
            self.stockMoveTable.setCellWidget(rowPosition,6,actionCombo)

    
    #add bar chart to widegt
    def add_bar_chart_to_widget(self, target_widget, data, categories, title="Bar Chart"):
        def clear_layout(widget):
            layout = widget.layout()
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    child = item.widget()
                    if child is not None:
                        child.setParent(None)

        clear_layout(target_widget)

        # Create a bar set and append data
        bar_set = QBarSet("Sales")
        bar_set.append(data)

        # Create a bar series and add the bar set
        series = QBarSeries()
        series.append(bar_set)

        # Create chart and configure
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(title)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        # Set up X and Y axes
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        try:
            axis_y.setRange(0, max(data) + 2)
        except:
            pass
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        # Create chart view
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        # Reuse existing layout or create a new one
        existing_layout = target_widget.layout()
        if existing_layout is None:
            layout = QVBoxLayout(target_widget)
            target_widget.setLayout(layout)
        else:
            layout = existing_layout

        layout.addWidget(chart_view)


    
    #Total items show in current store
    def loadTheTotalItemCountOfBussines(self):
        #load the inventry
        inventry = self.mydbfile.readData("./databases/inventry")
        count = 0

        for item in inventry:
            count = count + int(item["productCount"])
        
        #load the total of item count
        self.totalItemsCount.setText(str(count) + " +")

        pass

    #Total of the sold items Count
    def loadTheTotalItemCountOfSold(self):
        #load the shop data
        shopdata = self.mydbfile.readData("./databases/sale")
        count = 0
        for item in shopdata:
            if item["date"] == str(self.today):

                count = count + float(item["total"])

        #load the total of sold items of today
        self.totalSaleItemCount.setText("Rs. " + str(count) + " +")
        pass

    #available Categories
    def loadTheCountOfAvaiableCategories(self):
        inventry = self.mydbfile.readData("./databases/inventry")
        count = 0

        for item in inventry:
            if int(item["productCount"]) > 0:
                count = count + 1

        self.availableCategoriesCount.setText(str(count) + " +")
        pass
    
    #sale begin date & end date load
    def loadTheSaleDates(self):
        #Sale Date-------------------------------------------------------------------------------
        #assign the begin date
        self.saleBeginDate.setDate(QDate(
            int(datetime.datetime.now().year),
            int(datetime.datetime.now().month),
            (int(datetime.datetime.now().day)-2)
            ))
        
        #set the date format
        self.saleBeginDate.setDisplayFormat("dd/MM/yyyy")

        #set calender popup
        self.saleBeginDate.setCalendarPopup(True)

        #assign the end date
        self.saleEndDate.setDate(QDate(
            int(datetime.datetime.now().year),
            int(datetime.datetime.now().month),
            (int(datetime.datetime.now().day)+2)
            ))
        
        #set the date format
        self.saleEndDate.setDisplayFormat("dd/MM/yyyy")

        #set calender popup
        self.saleEndDate.setCalendarPopup(True)


        #call the sale report
        self.loadTheSaleReportBarChart()

       
        pass
    
    #load the sale report bar chart
    def loadTheSaleReportBarChart(self):
        #today = datetime.datetime.now()
        sale_dict = {}
        saleAmount = []
        saleDate = []
        shopdata = self.mydbfile.readData("./databases/sale")

        for item in shopdata:
            date = item["date"]
            if date not in sale_dict:
                # Only calculate totals once per date
                dataOfDay = self.mydbfile.searchData("./databases/sale", "date", date)
                total = sum(data["total"] for data in dataOfDay)
                sale_dict[date] = total

        # Convert to list of dictionaries (if needed for compatibility)
        from datetime import datetime

        sales = [{date: total} for date, total in sale_dict.items()]

        

        for sale in sales:
            for date_str, amount in sale.items():
                # Convert date string to datetime.date
                date_obj = datetime.strptime(date_str, "%Y/%m/%d").date()

                # Filter based on QDateEdit range
                if self.saleBeginDate.date().toPython() <= date_obj <= self.saleEndDate.date().toPython():
                    # Format for display (e.g., 'Jul-22') and collect data
                    saleDate.append(date_obj.strftime("%b-%d"))
                    saleAmount.append(amount)

        

        try:
            self.add_bar_chart_to_widget(
                self.mainWindow.salesChart, 
                saleAmount, 
                saleDate,
                title="Sale Report"
                )
            
            #print(saleAmount,saleDate)
        
        except Exception as e:
            self.infoMessage("Bar Chart Load Status",f"There is an error in Bar Chart Loading ! {e}")
        
        pass

        

SaleAnalyzer1 = SaleAnalyzer()