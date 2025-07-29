from fpdf import FPDF
import os
def create_pdf_report(context, as_bytes=False, output_file="report.pdf"):
    try:
        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, f"Risk Report for {context['ticker']}", ln=True, align="C")

        pdf.ln(10)
        pdf.cell(200, 10, f"Volatility: {context['volatility']}", ln=True)
        pdf.cell(200, 10, f"Sharpe Ratio: {context['sharpe_ratio']}", ln=True)
        pdf.cell(200, 10, f"Max Drawdown: {context['max_drawdown']}%", ln=True)

        if context.get("price_plot") and os.path.exists(context["price_plot"]):
            pdf.ln(10)
            pdf.image(context["price_plot"], x=10, w=180)

        if context.get("return_plot") and os.path.exists(context["return_plot"]):
            pdf.ln(10)
            pdf.image(context["return_plot"], x=10, w=180)

        if as_bytes:
            output = pdf.output(dest="S")
            return bytes(output)  # ✅ return only bytes
        else:
            pdf.output(output_file)
            return None  # ✅ consistent: return None when not in byte mode

    except Exception as e:
        print("PDF generation failed:", e)
        return None
