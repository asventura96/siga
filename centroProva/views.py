from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.forms import inlineformset_factory
from django.core.paginator import Paginator
from django.urls import reverse
from .models import CentroProva, CentroProvaExame, Aluno, Certificacao
from .forms import CentroProvaForm, CentroProvaExameForm

# View para a Página Inicial do Projeto
@login_required
def home(request):
    return render(request, 'home.html')

# View para a Página de Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redireciona para a página inicial
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# View para a Página Inicial do Centro de Provas
def centroProva_home(request):
    return render(request, 'centroProva/centroProva_home.html')

# CRUD Centro de Provas
def centroProva_new(request):
    if request.method == 'POST':
        form = CentroProvaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('centroProva_list'))
    else:
        form = CentroProvaForm()
    return render(request, 'centroProva/centroProva_form.html', {'form': form})

def centroProva_list(request):
    query = request.GET.get('q')  # Obtém o termo de busca da URL
    inativo = request.GET.get('inativo')  # Obtém o filtro de status (inativo)

    # Ordenação
    order_by = request.GET.get('order_by', 'nome')  # Define a ordenação padrão por Nome
    descending = request.GET.get('descending', 'False') == 'True'  # Verifica se é para ordenar de forma descendente

    # Inicializa a variável centroProva
    centroProva = CentroProva.objects.all()

    # Aplicar os filtros e pesquisa
    if query:
        centroProva = centroProva.filter(nome__icontains=query)  # Pesquisa por nome (parcial)
    if inativo:
        centroProva = centroProva.filter(inativo=inativo)  # Filtra por status

    # Aplicar ordenação
    if descending:
        order_by = f'-{order_by}'
    centroProva = centroProva.order_by(order_by)

    return render(request, 'centroProva/centroProva_list.html', {'centroProva': centroProva})

def centroProva_detail(request, pk):
    centroProva = get_object_or_404(CentroProva, pk=pk)
    return render(request, 'centroProva/centroProva_detail.html', {'centroProva': centroProva})

def centroProva_edit(request, pk):
    centroProva = get_object_or_404(CentroProva, pk=pk)
    if request.method == "POST":
        form = CentroProvaForm(request.POST, instance=centroProva)
        if form.is_valid():
            form.save()
            return redirect('centroProva_list')
    else:
        form = CentroProvaForm(instance=centroProva)
    return render(request, 'centroProva/centroProva_form.html', {'form': form})

def centroProva_delete(request, pk):
    centroProva = get_object_or_404(CentroProva, pk=pk)
    if request.method == "POST":
        centroProva.delete()
        return redirect('centroProva_list')
    return render(request, 'centroProva/centroProva_confirmDelete.html', {'centroProva': centroProva})

def centroProva_reports(request):
    # Placeholder para a funcionalidade de relatórios
    return render(request, 'centroProva/centroProva_reports.html')

# CRUD Exames
def exame_new(request):
    if request.method == 'POST':
        form = CentroProvaExameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('exame_list'))
    else:
        form = CentroProvaExameForm()
    return render(request, 'centroProva/centroProva-exame_form.html', {'form': form})

def exame_list(request):
    # Obtém os filtros
    data_inicio = request.GET.get('data_inicio')  # Data de início do período
    data_fim = request.GET.get('data_fim')        # Data de fim do período
    presenca = request.GET.get('presenca')         # Filtro por Presença
    cancelado = request.GET.get('cancelado')       # Filtro de Exame Cancelado
    aluno = request.GET.get('aluno')               # Filtro de Aluno
    centroProva = request.GET.get('centroProva')   # Filtro de Centro de Provas
    certificacao = request.GET.get('certificacao')  # Filtro de Certificação

    # Ordenação
    order_by = request.GET.get('order_by', 'data')  # Define a ordenação padrão por Data
    descending = request.GET.get('descending', 'False') == 'True'  # Verifica se é para ordenar de forma descendente

    # Otimização de Consulta
    centroProva_exame = CentroProvaExame.objects.select_related('aluno', 'centroProva', 'certificacao')

    # Aplicar os filtros e pesquisa
    if data_inicio and data_fim:
        centroProva_exame = centroProva_exame.filter(data__range=[data_inicio, data_fim])  # Filtro de Data para um intervalo
    elif data_inicio:
        centroProva_exame = centroProva_exame.filter(data__gte=data_inicio)  # Filtro a partir da data de início
    elif data_fim:
        centroProva_exame = centroProva_exame.filter(data__lte=data_fim)  # Filtro até a data de fim

    if presenca:
        centroProva_exame = centroProva_exame.filter(presenca=presenca)  # Pesquisa Presença
    if cancelado:
        centroProva_exame = centroProva_exame.filter(cancelado=cancelado)  # Pesquisa Cancelado
    if aluno:
        centroProva_exame = centroProva_exame.filter(aluno__nome=aluno)  # Pesquisa Aluno
    if centroProva:
        centroProva_exame = centroProva_exame.filter(centroProva__nome=centroProva)  # Pesquisa Centro de Prova
    if certificacao:
        centroProva_exame = centroProva_exame.filter(certificacao__nome=certificacao)  # Pesquisa Certificação

    # Aplicar ordenação
    if descending:
        order_by = f'-{order_by}'
    centroProva_exame = centroProva_exame.order_by(order_by)

    # Paginação
    records_per_page = request.GET.get('records_per_page', 10)  # Padrão: 10 registros por página
    try:
        records_per_page = int(records_per_page)
    except (ValueError, TypeError):
        records_per_page = 10  # Caso ocorra erro, volta para o padrão de 10

    paginator = Paginator(centroProva_exame, records_per_page)  # Cria o paginator
    page_number = request.GET.get('page')  # Obtém o número da página atual
    centroProva_exame_page = paginator.get_page(page_number)  # Pega a página solicitada

    # Buscar e ordenar
    centroProva_exame = CentroProvaExame.objects.select_related('aluno', 'centro_prova', 'certificacao')
    alunos = Aluno.objects.order_by('nome')
    centrosProva = CentroProva.objects.order_by('nome')
    certificacoes = Certificacao.objects.order_by('descricao')

    return render(request, 'centroProva/centroProva-exame_list.html', {
        'centroProva_exame': centroProva_exame_page,
        'aluno': alunos,
        'centroProva': centrosProva,
        'certificacao': certificacoes,
    })

def exame_detail(request, pk):
    centroProva_exame = get_object_or_404(CentroProvaExame, pk=pk)
    return render(request, 'centroProva/centroProva-exame_detail.html', {'centroProva_exame': centroProva_exame})

def exame_reports(request):
    # Placeholder para a funcionalidade de relatórios
    return render(request, 'centroProva/centroProva-exame_reports.html')
