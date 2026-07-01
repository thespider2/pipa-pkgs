#!/usr/bin/bash

install_optional_dirs() {
    local dir

    for dir in "$@"; do
        [[ -d "$dir" ]] || continue
        inst_dir "$dir"
    done
}

install_optional_firmware() {
    local firmware

    for firmware in "$@"; do
        [[ -e "$firmware" ]] || continue
        inst "$firmware"
    done
}

# called by dracut
install() {
    install_optional_dirs \
        "/usr/lib/firmware" \
        "/usr/lib/firmware/ath11k" \
        "/usr/lib/firmware/qca" \
        "/usr/lib/firmware/qcom/sm8250/xiaomi/pipa"

    install_optional_firmware \
        "/usr/lib/firmware/qcom/a650_sqe.fw" \
        "/usr/lib/firmware/qcom/a650_gmu.bin" \
        "/usr/lib/firmware/qcom/sm8250/xiaomi/pipa/a650_zap.mbn" \
        "/usr/lib/firmware/qcom/sm8250/xiaomi/pipa/adspr.jsn" \
        "/usr/lib/firmware/qcom/sm8250/xiaomi/pipa/cdsp.mbn" \
        "/usr/lib/firmware/qcom/sm8250/xiaomi/pipa/slpi.mbn" \
        "/usr/lib/firmware/qcom/sm8250/xiaomi/pipa/slpius.jsn" \
        "/usr/lib/firmware/qcom/sm8250/xiaomi/pipa/adsp.mbn" \
        "/usr/lib/firmware/qcom/sm8250/xiaomi/pipa/adspua.jsn" \
        "/usr/lib/firmware/qcom/sm8250/xiaomi/pipa/cdspr.jsn" \
        "/usr/lib/firmware/qcom/sm8250/xiaomi/pipa/slpir.jsn" \
        "/usr/lib/firmware/qcom/sm8250/xiaomi/pipa/venus.mbn" \
        "/usr/lib/firmware/nuvolta/rx1665.bin" \
        "/usr/lib/firmware/awinic/aw88230_2113_pipa.bin" \
        "/usr/lib/firmware/novatek/nt36532_csot.bin" \
        "/usr/lib/firmware/novatek/nt36532_tianma.bin" \
        "/usr/lib/firmware/qca/hpnv21g.309" \
        "/usr/lib/firmware/qca/nvm_usb_00130201_gf.bin" \
        "/usr/lib/firmware/qca/nvm_00440302_i2s_eu.bin" \
        "/usr/lib/firmware/qca/hpnv21.bb8" \
        "/usr/lib/firmware/qca/hpnv21.baa" \
        "/usr/lib/firmware/qca/hpnv21g.b10c" \
        "/usr/lib/firmware/qca/htbtfw20.tlv" \
        "/usr/lib/firmware/qca/rampatch_00130302.bin" \
        "/usr/lib/firmware/qca/hmtnv20.bin" \
        "/usr/lib/firmware/qca/nvm_00130302.bin" \
        "/usr/lib/firmware/qca/hpnv21g.ba3" \
        "/usr/lib/firmware/qca/apbtfw11.tlv" \
        "/usr/lib/firmware/qca/hmtnv20.b10f" \
        "/usr/lib/firmware/qca/nvm_usb_00130200.bin" \
        "/usr/lib/firmware/qca/apbtfw10.tlv" \
        "/usr/lib/firmware/qca/rampatch_00440302.bin" \
        "/usr/lib/firmware/qca/hpnv21g.b8c" \
        "/usr/lib/firmware/qca/hpnv21g.baa" \
        "/usr/lib/firmware/qca/nvm_usb_00000300.bin" \
        "/usr/lib/firmware/qca/nvm_00440302_eu.bin" \
        "/usr/lib/firmware/qca/crnv32.bin" \
        "/usr/lib/firmware/qca/nvm_usb_00130201.bin" \
        "/usr/lib/firmware/qca/hpnv21g.bb8" \
        "/usr/lib/firmware/qca/nvm_usb_00130200_0104.bin" \
        "/usr/lib/firmware/qca/hpbtfw21.tlv" \
        "/usr/lib/firmware/qca/apnv10.bin" \
        "/usr/lib/firmware/qca/hpnv21.ba3" \
        "/usr/lib/firmware/qca/rampatch_usb_00190200.bin" \
        "/usr/lib/firmware/qca/apnv11.bin" \
        "/usr/lib/firmware/qca/hpnv21g.ba1" \
        "/usr/lib/firmware/qca/hpnv21.b9f" \
        "/usr/lib/firmware/qca/rampatch_usb_00130201.bin" \
        "/usr/lib/firmware/qca/crnv21.bin" \
        "/usr/lib/firmware/qca/msnv11.b09" \
        "/usr/lib/firmware/qca/nvm_usb_00000200.bin" \
        "/usr/lib/firmware/qca/rampatch_usb_00000300.bin" \
        "/usr/lib/firmware/qca/msbtfw11.tlv" \
        "/usr/lib/firmware/qca/crbtfw21.tlv" \
        "/usr/lib/firmware/qca/nvm_usb_00130201_gf_0303.bin" \
        "/usr/lib/firmware/qca/nvm_usb_00130200_0107.bin" \
        "/usr/lib/firmware/qca/nvm_usb_00130201_0303.bin" \
        "/usr/lib/firmware/qca/rampatch_usb_00130200.bin" \
        "/usr/lib/firmware/qca/hpnv21.b8c" \
        "/usr/lib/firmware/qca/hpnv21.b10c" \
        "/usr/lib/firmware/qca/crnv32u.bin" \
        "/usr/lib/firmware/qca/nvm_00440302.bin" \
        "/usr/lib/firmware/qca/rampatch_usb_00000302.bin" \
        "/usr/lib/firmware/qca/nvm_usb_00000302.bin" \
        "/usr/lib/firmware/qca/hpnv21.301" \
        "/usr/lib/firmware/qca/nvm_00130300.bin" \
        "/usr/lib/firmware/qca/msnv11.b0a" \
        "/usr/lib/firmware/qca/hpnv21.ba1" \
        "/usr/lib/firmware/qca/msbtfw11.mbn" \
        "/usr/lib/firmware/qca/rampatch_00230302.bin" \
        "/usr/lib/firmware/qca/htnv20.bin" \
        "/usr/lib/firmware/qca/nvm_usb_00000302_eu.bin" \
        "/usr/lib/firmware/qca/hpnv21g.301" \
        "/usr/lib/firmware/qca/nvm_00230302.bin" \
        "/usr/lib/firmware/qca/hpnv21.309" \
        "/usr/lib/firmware/qca/crbtfw32.tlv" \
        "/usr/lib/firmware/qca/msnv11.bin" \
        "/usr/lib/firmware/qca/nvm_usb_00190200.bin" \
        "/usr/lib/firmware/qca/rampatch_usb_00000200.bin" \
        "/usr/lib/firmware/qca/hpnv21g.b9f" \
        "/usr/lib/firmware/qca/rampatch_00130300.bin" \
        "/usr/lib/firmware/qca/hmtbtfw20.tlv"
}
