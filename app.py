def pdf_expander_ui(res, df, fig, contexto_base: dict):
    """Bloco para gerar PDF de relatório com fallbacks (zip e preview inline)."""
    import base64, io, zipfile
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

    contexto = dict(contexto_base)
    contexto.update({"obra": obra, "cliente": cliente, "engenheiro": engenheiro, "crea": crea, "obs": obs})

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
            # download normal
            st.download_button(
                "⬇️ Baixar PDF",
                data=st.session_state["pdf_report_data"],
                file_name=st.session_state.get("pdf_report_name", "relatorio_catenaria.pdf"),
                mime="application/pdf",
                use_container_width=True,
                key="pdf_download_btn"
            )

            # fallback ZIP
            with io.BytesIO() as zbuf:
                with zipfile.ZipFile(zbuf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
                    zf.writestr(st.session_state.get("pdf_report_name","relatorio_catenaria.pdf"),
                                st.session_state["pdf_report_data"])
                zbytes = zbuf.getvalue()
            st.download_button(
                "⬇️ Baixar como ZIP (fallback)",
                data=zbytes,
                file_name="relatorio_catenaria.zip",
                mime="application/zip",
                use_container_width=True,
                key="pdf_zip_btn"
            )

            # preview inline (imprimir/salvar pelo navegador)
            with st.expander("👀 Pré-visualização (se bloqueia download, use Imprimir → Salvar como PDF)"):
                b64 = base64.b64encode(st.session_state["pdf_report_data"]).decode("utf-8")
                html_iframe = f'''
                    <iframe
                        src="data:application/pdf;base64,{b64}"
                        width="100%" height="700px" style="border:1px solid #444;">
                    </iframe>
                '''
                st.components.v1.html(html_iframe, height=720)
        else:
            st.info("Gere o PDF para habilitar o download e a pré-visualização.")


def word_expander_ui(res, df, fig, contexto_base: dict):
    """Bloco para gerar Word com fallback em ZIP (políticas corporativas às vezes barram .docx)."""
    import io, zipfile
    st.markdown("### 📝 Relatório técnico (Word)")

    c1, c2 = st.columns(2)
    with c1:
        obra = st.text_input("Obra / Identificação", value=contexto_base.get("obra",""), key="word_obra")
        cliente = st.text_input("Cliente / Unidade", value=contexto_base.get("cliente",""), key="word_cliente")
        engenheiro = st.text_input("Engenheiro responsável", value=contexto_base.get("engenheiro",""), key="word_eng")
    with c2:
        crea = st.text_input("CREA", value=contexto_base.get("crea",""), key="word_crea")
        obs = st.text_area("Observações", value=contexto_base.get("obs",""), height=90, key="word_obs")

    contexto = dict(contexto_base)
    contexto.update({"obra": obra, "cliente": cliente, "engenheiro": engenheiro, "crea": crea, "obs": obs})

    def _gen_word():
        try:
            word_bytes = build_word_report_bytes(contexto, res, df, fig)
            st.session_state["word_report_data"] = word_bytes
            st.session_state["word_report_name"] = "relatorio_catenaria.docx"
            st.toast("Word gerado com sucesso!", icon="✅")
        except Exception as e:
            st.session_state["word_report_error"] = str(e)

    col_btn, col_down = st.columns([1, 1])
    with col_btn:
        st.button("📝 Gerar/Atualizar Word do relatório",
                  type="secondary",
                  use_container_width=True,
                  on_click=_gen_word)

    with col_down:
        if "word_report_error" in st.session_state:
            st.error(f"Falha ao gerar Word: {st.session_state['word_report_error']}")
            del st.session_state["word_report_error"]

        if "word_report_data" in st.session_state:
            # download normal
            st.download_button(
                "⬇️ Baixar DOCX",
                data=st.session_state["word_report_data"],
                file_name=st.session_state.get("word_report_name", "relatorio_catenaria.docx"),
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
                key="word_download_btn"
            )

            # fallback ZIP
            with io.BytesIO() as zbuf:
                with zipfile.ZipFile(zbuf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
                    zf.writestr(st.session_state.get("word_report_name","relatorio_catenaria.docx"),
                                st.session_state["word_report_data"])
                zbytes = zbuf.getvalue()
            st.download_button(
                "⬇️ Baixar como ZIP (fallback)",
                data=zbytes,
                file_name="relatorio_catenaria_docx.zip",
                mime="application/zip",
                use_container_width=True,
                key="word_zip_btn"
            )
        else:
            st.info("Gere o Word para habilitar o download.")
