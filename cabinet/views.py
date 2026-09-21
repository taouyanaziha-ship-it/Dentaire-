from django.shortcuts import redirect, render,get_object_or_404
from.forms import PatientForm, DentisteForm, RendezvousForm
from .models import Patient, Dentiste, Rendezvous
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from .models import Recu
from .forms import RecuForm



def home(request):
    total_patients   = Patient.objects.count()
    total_dentistes  = Dentiste.objects.count()
    total_rendezvous = Rendezvous.objects.count()
    derniers_rdv      = Rendezvous.objects.order_by('-date')[:3]
    derniers_paiements = Recu.objects.order_by('-date_paiement')[:3]
    rdv_payes         = Rendezvous.objects.filter(recu__isnull=False)
    rdv_impayes       = Rendezvous.objects.filter(recu__isnull=True)
    total_paye        = sum(r.montant for r in Recu.objects.all()) or 0

    return render(request, 'cabinet/home.html', {
        'total_patients':    total_patients,
        'total_dentistes':   total_dentistes,
        'total_rendezvous':  total_rendezvous,
        'derniers_rdv':      derniers_rdv,
        'derniers_paiements': derniers_paiements,
        'rdv_payes':         rdv_payes,
        'rdv_impayes':       rdv_impayes,
        'total_paye':        total_paye,
    })

def patients_list(request):
    patients = Patient.objects.all()
    return render(request, 'cabinet/patients_list.html', {'patients': patients})

def ajouter_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patients_list')
    else:
        form = PatientForm()

    return render(request, 'cabinet/ajouter_patient.html', {'form': form})
 
def dentistes_list(request):
    dentistes = Dentiste.objects.all()
    return render(request,'cabinet/dentistes_list.html',{'dentistes':dentistes})

def ajouter_dentistes(request):
    if request.method == 'POST':
        form = DentisteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dentistes_list')
    else:
        form = DentisteForm()

    return render(request, 'cabinet/ajouter_dentistes.html', {'form': form})

def rendezvous_list(request):
    rendezvous = Rendezvous.objects.all()
    return render(request, 'cabinet/rendezvous_list.html', {'rendezvous': rendezvous})

def ajouter_rendezvous(request):
    if request.method == 'POST':
        form = RendezvousForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rendezvous_list')
    else:
        form = RendezvousForm()

    return render(request, 'cabinet/ajouter_rendezvous.html', {'form': form})
def paiements(request):
    rdv_payes   = Rendezvous.objects.filter(recu__isnull=False)
    rdv_impayes = Rendezvous.objects.filter(recu__isnull=True)
    return render(request, 'cabinet/paiements.html', {
        'rdv_payes':   rdv_payes,
        'rdv_impayes': rdv_impayes,
    })

def recu_ajouter(request, rdv_id):
    rdv  = get_object_or_404(Rendezvous, pk=rdv_id)
    form = RecuForm(request.POST or None)
    if form.is_valid():
        recu = form.save(commit=False)
        recu.rendezvous = rdv
        recu.save()
        return redirect('recu_detail', pk=recu.pk)
    return render(request, 'cabinet/recu_form.html', {'form': form, 'rdv': rdv})

def recu_detail(request, pk):
    recu = get_object_or_404(Recu, pk=pk)
    return render(request, 'cabinet/recu_detail.html', {'recu': recu})

def recu_pdf(request, pk):
    recu     = get_object_or_404(Recu, pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="recu_{recu.id}.pdf"'
    p    = canvas.Canvas(response, pagesize=A4)
    w, h = A4

    p.setFillColorRGB(0.17, 0.70, 0.64)
    p.rect(0, h-100, w, 100, fill=1, stroke=0)
    p.setFillColorRGB(1, 1, 1)
    p.setFont("Helvetica-Bold", 22)
    p.drawString(50, h-55, "Cabinet Dentaire")
    p.setFont("Helvetica", 12)
    p.drawString(50, h-80, "Reçu de Paiement")

    p.setFillColorRGB(0.1, 0.1, 0.1)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, h-140, f"Reçu N° : {recu.id:04d}")
    p.setFont("Helvetica", 11)
    p.drawString(50, h-165, f"Date : {recu.date_paiement.strftime('%d/%m/%Y')}")

    p.setStrokeColorRGB(0.17, 0.70, 0.64)
    p.setLineWidth(1.5)
    p.line(50, h-185, w-50, h-185)

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, h-215, "Informations Patient :")
    p.setFont("Helvetica", 11)
    p.drawString(50, h-235, f"Nom      : {recu.rendezvous.patient}")
    p.drawString(50, h-255, f"Dentiste : {recu.rendezvous.dentiste}")
    p.drawString(50, h-275, f"Date RDV : {recu.rendezvous.date.strftime('%d/%m/%Y')}")
    p.drawString(50, h-295, f"Heure    : {recu.rendezvous.heure.strftime('%H:%M')}")
    p.drawString(50, h-315, f"Motif    : {recu.rendezvous.motif}")

    p.line(50, h-335, w-50, h-335)

    p.setFont("Helvetica-Bold", 13)
    p.drawString(50, h-365, f"Mode : {recu.get_mode_paiement_display()}")
    p.setFillColorRGB(0.17, 0.70, 0.64)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, h-400, f"Montant : {recu.montant} MAD")

    p.setFillColorRGB(0.5, 0.5, 0.5)
    p.setFont("Helvetica", 9)
    p.drawString(50, 40, "Merci de votre confiance — Cabinet Dentaire")

    p.showPage()
    p.save()
    return response