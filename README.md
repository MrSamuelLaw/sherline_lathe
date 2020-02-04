# sherline_lathe
CNC_TOOLBOX wb for UTA Fablab Sherline Lathe single turrent

How to use
1. Make sure you have CNC_TOOLBOX downloaded and able to open up
2. Make a folder named "sherline_lathe" in the "wb" folder located in CNC_TOOLBOX (the naming is important)
3. Copy and Paste all of the files from the this repository into the folder you just created
4. Restart CNC_TOOLBOX
5. Verify that you are now able to select the Sherline Lathe from the device drop down menu

NOTES:
  - to edit tool table function to always overwrite a file, rather than letting you select a folder
    in the file my_sherline_lathe_wb.py in the generate_tool_table, delete the following:
    
    browser = QFileDialog()
        browser.setFileMode(QFileDialog.DirectoryOnly)
        if browser.exec_():
            folder = browser.selectedFiles()[0]
     and replace with folder = "path/to/your/directory"
     
     The function will now overwrite the same file every time
