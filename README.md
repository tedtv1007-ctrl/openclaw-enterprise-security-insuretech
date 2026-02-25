# OpenClaw Enterprise Security for InsureTech

專案目標：針對產險業（InsureTech）的高度安全需求，利用 OpenClaw 建立安全可靠的自動化理賠與安全部署流程。

## 🛡️ 安全架構目標
1. **多租戶隔離**: 利用 Kubernetes Namespace 與 Network Policies 隔離不同部門的 AI Agent 執行環境。
2. **敏感資料去識別化 (DLP)**: 在資料傳輸至 LLM 前，自動偵測並遮蔽身分證字號、車牌號碼、診斷證明等敏感資訊。
3. **稽核日誌 (Audit Logs)**: 記錄所有與 AI 的交互，確保符合金管會對金融雲端服務的資安規範。

## ⚡ 理賠效率優化流程 (Claim Automation)
- **OCR 預處理**: 串接 MCP 工具進行理賠文件自動辨識。
- **規則引擎校驗**: AI 助理比對保單條款與事故資料，進行初步理賠試算。
- **異常偵測**: 識別可能的保險詐欺行為特徵並標註提醒。

## 📍 目前進度
- [ ] 基礎環境架構規劃
- [ ] 產險理賠情境 MCP Tool 設計
- [ ] 資料脫敏 (Data Masking) 技術研究
