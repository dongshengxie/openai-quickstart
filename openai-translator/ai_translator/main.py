import sys
import os
import gradio as gr
from utils.logger import Logger

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, ConfigLoader, LOG
from model import GLMModel, OpenAIModel
from translator import PDFTranslator

def translation(input_file, file_format, target_language, path, pages):
    LOG.debug(f"[翻译任务]\n源文件: {input_file.name}\n目标语言: {target_language}\n路径: {path}\n页数: {pages}")
    pg = int(pages)
    output_file_path = Translator.translate_pdf(
        input_file.name,  file_format = file_format, target_language=target_language, output_file_path = path, pages = pg)

    return output_file_path

def launch_gradio():
    iface = gr.Interface(
        fn=translation,
        title="OpenAI-Translator v2.0",
        inputs=[
            gr.File(label="上传PDF文件"),
            gr.Textbox(label="文件类型"),
            gr.Textbox(label="目标语言（默认：中文）", placeholder="Chinese", value="Chinese"),
            gr.Textbox(label="输出路径"),
            gr.Textbox(label="页数")
        ],
        outputs=[
            gr.File(label="下载翻译文件")
        ]
    )
    iface.launch(share=True)

if __name__ == "__main__":
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()
    config_loader = ConfigLoader(args.config)

    config = config_loader.load_config()

    model_name = args.openai_model if args.openai_model else config['OpenAIModel']['model']
    api_key = args.openai_api_key if args.openai_api_key else config['OpenAIModel']['api_key']
    model = OpenAIModel(model=model_name, api_key=api_key)


    pdf_file_path = args.book if args.book else config['common']['book']
    file_format = args.file_format if args.file_format else config['common']['file_format']

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    global Translator
    Translator = PDFTranslator(model)
    # translator.translate_pdf(pdf_file_path, file_format)

    launch_gradio()



