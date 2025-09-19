def pdf_expander_ui(res, df, fig, contexto_base: dict):
    """Bloco UI para preencher cabeçalho e baixar PDF (robusto, com callback)."""
    st.markdown("### 📄 Relatório técnico (PDF)")

    # --------- campos do cabeçalho ---------
    c1, c2 = st.columns(2)
    with c1:
        obra = st.text_input("Obra / Identificação", value=contexto_base.get("obra",""), key="pdf_obra")
        cliente = st.text_input("Cliente / Unidade", value=contexto_base.get("cliente",""), key="pdf_cliente")
        engenheiro = st.text_input("Engenheiro responsável", value=contexto_base.get("engenheiro",""), key="pdf_eng")
    with c2:
        crea = st.text_input("CREA", value=contexto_base.get("crea",""), key="pdf_crea")
        obs = st.text_area("Observações", value=contexto_base.get("obs",""), height=90, key="pdf_obs")

    # Monta contexto atual dos campos
    contexto = dict(contexto_base)
    contexto.update({"obra": obra, "cliente": cliente, "engenheiro": engenheiro, "crea": crea, "obs": obs})

    # --------- callback que gera e grava no session_state ---------
    def _gen_pdf():
        try:
            pdf_bytes = build_pdf_report_bytes(contexto, res, df, fig)
            st.session_state["pdf_report_data"] = pdf_bytes
            st.session_state["pdf_report_name"] = "relatorio_catenaria.pdf"
            st.toast("PDF gerado com sucesso!", icon="✅")
        except Exception as e:
            st.session_state["pdf_report_error"] = str(e)

    col_btn, col_down = st.columns([1, 1])
    with col_btn:
        st.button("📄 Gerar/Atualizar PDF do relatório",
                  type="secondary",
                  use_container_width=True,
                  on_click=_gen_pdf)

    with col_down:
        if "pdf_report_error" in st.session_state:
            st.error(f"Falha ao gerar PDF: {st.session_state['pdf_report_error']}")
            del st.session_state["pdf_report_error"]

        if "pdf_report_data" in st.session_state:
            st.download_button(
                "⬇️ Baixar PDF",
                data=st.session_state["pdf_report_data"],
                file_name=st.session_state.get("pdf_report_name", "relatorio_catenaria.pdf"),
                mime="application/pdf",
                use_container_width=True,
                key="pdf_download_btn"
            )
        else:
            st.info("Gere o PDF para habilitar o download.")
