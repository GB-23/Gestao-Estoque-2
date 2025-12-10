# Obsoleto, mantido pra mostrar na aula


class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    idade: int | None = None
    funcao: str | None = None
    cpf: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    senha: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def validar_token_rapido(db: Session, codigo: str) -> QuickToken | None:
    qt = db.query(QuickToken).filter(QuickToken.codigo == codigo).first()
    if not qt:
        return None
    if qt.expira_em < datetime.utcnow():
        return None
    return qt



@router.post("/auth/register")
def register(payload: UserCreate, db: Session = Depends(get_db)):

    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    if payload.cpf and db.query(User).filter(User.cpf == payload.cpf).first():
        raise HTTPException(status_code=400, detail="CPF já cadastrado")

    user = User(
        nome=payload.nome,
        idade=payload.idade,
        funcao=payload.funcao,
        email=payload.email,
        senha=payload.senha,   
        cpf=payload.cpf
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "status": "ok",
        "mensagem": "Usuário cadastrado",
        "id": user.id,
        "nome": user.nome
    }


@router.post("/auth/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == payload.email).first()

    if not user or user.senha != payload.senha:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    return {
        "status": "ok",
        "mensagem": "Login autorizado",
        "id": user.id,
        "nome": user.nome
    }


@router.post("/token_acesso_rapido")
def gerar_token_rapido(email: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    codigo = generate_code(7)
    agora = datetime.utcnow()
    expira = agora + timedelta(hours=6)

    qt = QuickToken(
        nome=user.nome,
        email=user.email,
        codigo=codigo,
        criado_em=agora,
        expira_em=expira
    )

    db.add(qt)
    db.commit()
    db.refresh(qt)

    return {"token": codigo, "expira_em": expira.isoformat()}


@router.get("/APISocket/{token}/adicionar_produto/{nome}/{preco}/{volume}/{validade}")
def adicionar_produto(
    token: str,
    nome: str,
    preco: float,
    volume: str,
    validade: str,
    db: Session = Depends(get_db)
):

    if not validar_token_rapido(db, token):
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    novo = Product(
        nome=nome,
        preco=preco,
        volume=volume,
        validade=validade,
        token_produto=generate_code(7)
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return {"status": "ok", "id": novo.id, "token_produto": novo.token_produto}


@router.get("/APISocket/{token}/editar_produto/{product_id}")
def editar_produto(token: str, product_id: int, nome: str | None = None,
                   preco: float | None = None, volume: str | None = None,
                   validade: str | None = None, db: Session = Depends(get_db)):

    if not validar_token_rapido(db, token):
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    produto = db.query(Product).filter(Product.id == product_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    antes = produto.__dict__.copy()

    if nome: produto.nome = nome
    if preco: produto.preco = preco
    if volume: produto.volume = volume
    if validade: produto.validade = validade

    db.commit()
    db.refresh(produto)

    edit = EditedItem(
        id_informacoes=str(product_id),
        token_item=produto.token_produto,
        informacoes_editadas=str(antes)
    )

    db.add(edit)
    db.commit()

    return {"status": "ok", "mensagem": "Produto atualizado"}


@router.get("/APISocket/{token}/listar_produtos")
def listar_produtos(token: str, db: Session = Depends(get_db)):

    if not validar_token_rapido(db, token):
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    produtos = db.query(Product).all()
    return [{
        "id": p.id,
        "nome": p.nome,
        "preco": p.preco,
        "volume": p.volume,
        "validade": p.validade,
        "token_produto": p.token_produto
    } for p in produtos]



@router.delete("/APISocket/{token}/deletar_produto/{product_id}")
def deletar_produto(token: str, product_id: int, db: Session = Depends(get_db)):

    if not validar_token_rapido(db, token):
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    produto = db.query(Product).filter(Product.id == product_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    registro = EditedItem(
        id_informacoes=str(product_id),
        token_item=produto.token_produto,
        informacoes_editadas="DELETADO"
    )

    db.add(registro)
    db.delete(produto)
    db.commit()

    return {"status": "ok", "mensagem": "Produto removido"}

