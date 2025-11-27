-- Tabelas de controle de uploads e erros (schema public)
CREATE TABLE IF NOT EXISTS public.arquivos_upload (
    id UUID PRIMARY KEY,
    nome_original TEXT NOT NULL,
    chave_s3 TEXT NOT NULL,
    status TEXT NOT NULL,
    tamanho BIGINT,
    mime TEXT,
    usuario TEXT,
    dt_upload TIMESTAMP DEFAULT NOW(),
    dt_validacao TIMESTAMP NULL,
    dt_importacao TIMESTAMP NULL,
    stats JSONB NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.arquivos_erros (
    id BIGSERIAL PRIMARY KEY,
    arquivo_id UUID NOT NULL REFERENCES public.arquivos_upload(id) ON DELETE CASCADE,
    codigo TEXT,
    descricao_codigo TEXT,
    mensagem TEXT,
    planilha TEXT,
    linha INT NULL,
    coluna TEXT,
    tipo TEXT,
    severidade TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Índices úteis
CREATE INDEX IF NOT EXISTS idx_arquivos_upload_status ON public.arquivos_upload(status);
CREATE INDEX IF NOT EXISTS idx_arquivos_erros_arquivo ON public.arquivos_erros(arquivo_id);

-- Tabela attachments genérica para associar outras entidades a arquivos
CREATE TABLE IF NOT EXISTS public.attachments (
    id UUID PRIMARY KEY,
    ref_tipo TEXT NOT NULL,
    ref_id TEXT NOT NULL,
    arquivo_id UUID NOT NULL REFERENCES public.arquivos_upload(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_attachments_ref ON public.attachments(ref_tipo, ref_id);