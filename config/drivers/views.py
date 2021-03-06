from itertools import chain

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .forms import DriverForm, EditDriverForm
from .models import Driver
from package.models import Package, Offer


@login_required
def submit_driver(request):
    form = DriverForm(data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('/driver/' + str(form.instance.slug))
    return render(request, "drivers/create-route.html", {
        'form': form})


@login_required
def list_drivers(request):
    if request.GET.get("q"):
        drivers_to = Driver.objects.filter(departure__contains=request.GET.get("q"))
        drivers_from = Driver.objects.filter(arrival__contains=request.GET.get("q"))
        drivers = list(chain(drivers_to, drivers_from))
        greeting = "Here's what we found"
    else:
        drivers = Driver.objects.order_by("-id").all()
        greeting = "Recent Drivers"
    return render(request, "list.html", {
        "type": "Drivers",
        "drivers": drivers,
        "greeting": greeting,
    })


@login_required
def driver(request, slug):
    drivers = get_object_or_404(Driver, slug=slug)
    if request.method == 'POST':
        if request.POST.get("deletePost") and drivers.author == request.user:
            drivers.delete()
            return redirect('/')
        else:
            package_id = request.POST.get("package-id")
            package = get_object_or_404(Package, id=package_id)
            offer = Offer(driver=drivers, package=package, driver_user=drivers.author, package_user=package.author)
            offer.save()
            
    return render(request, "drivers/post.html", {
        "package": drivers,
        "user": request.user,
        "packages": Package.objects.filter(author=request.user)
    })


@login_required
def edit_drivers(request, slug):
    post = get_object_or_404(Driver, slug=slug)
    if post.author != request.user:
        return HttpResponseForbidden()
    form = EditDriverForm(request.POST or None, request.FILES or None,
                          instance=post)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/driver/' + post.slug)
    return render(request, 'drivers/edit_rout.html', {
        'post': post,
        'form': form,
    })
