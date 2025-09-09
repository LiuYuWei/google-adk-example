# 設定虛擬環境
setup:
	python3 -m venv venv
	source venv/bin/activate

# 安裝相依套件
install:
	./venv/bin/pip install -r requirements.txt

# 啟動 agent 伺服器
run:
	adk web

# .PHONY 避免與同名檔案衝突
.PHONY: setup install run
