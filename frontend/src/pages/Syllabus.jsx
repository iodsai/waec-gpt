import React, { useEffect, useMemo, useState } from "react";
import { Link, useParams, useSearchParams } from "react-router-dom";
import http from "@/lib/api";
import {
  ArrowLeft,
  BookOpen,
  CheckCircle2,
  ChevronRight,
  FileText,
  Flag,
  Layers3,
  Map,
} from "lucide-react";

const COUNTRY_LABELS = {
  all: "All",
  nigeria: "Nigeria",
  ghana: "Ghana",
};

const countryBadgeClass = {
  general: "!bg-sand !text-moss !border-edge",
  nigeria: "!bg-terracotta/10 !text-terracotta !border-terracotta/30",
  ghana: "!bg-success/10 !text-success !border-success/30",
};

const CountryBadge = ({ country = "general" }) => (
  <span className={`tag ${countryBadgeClass[country] || countryBadgeClass.general}`}>
    {country === "general" ? "Common" : `${COUNTRY_LABELS[country]} only`}
  </span>
);

const statusLabel = {
  lesson_available: "Lesson ready",
  topic_available: "Topic mapped",
  needs_course_buildout: "Needs lesson build-out",
};

const statusClass = {
  lesson_available: "!text-success !bg-success/10 !border-success/30",
  topic_available: "!text-moss !bg-moss/10 !border-moss/30",
  needs_course_buildout: "!text-muted2 !bg-sand !border-edge",
};

const Syllabus = () => {
  const { itemId } = useParams();
  const [params, setParams] = useSearchParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const country = params.get("country") || "all";

  useEffect(() => {
    http.get("/syllabus")
      .then((r) => setData(r.data))
      .finally(() => setLoading(false));
  }, []);

  const flatItems = useMemo(() => {
    if (!data) return [];
    return data.sections.flatMap((section) =>
      section.items.map((item) => ({ ...item, section_id: section.id, section_name: section.name }))
    );
  }, [data]);

  const activeItem = flatItems.find((item) => item.id === itemId);

  const setCountry = (next) => {
    const p = new URLSearchParams(params);
    if (next === "all") p.delete("country"); else p.set("country", next);
    setParams(p, { replace: true });
  };

  const visibleCountryDetails = (item) => {
    const details = item?.country_details || [];
    if (country === "all") return details;
    return details.filter((detail) => detail.country === country);
  };

  if (loading) return <div className="p-10 text-muted2">Loading syllabus...</div>;
  if (!data) return <div className="p-10 text-muted2">Syllabus unavailable.</div>;

  if (itemId) {
    if (!activeItem) return <div className="p-10 text-muted2">Syllabus item not found.</div>;
    const countryDetails = visibleCountryDetails(activeItem);

    return (
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-12 py-10" data-testid={`syllabus-detail-${activeItem.id}`}>
        <Link to={`/syllabus${country === "all" ? "" : `?country=${country}`}`} className="inline-flex items-center gap-2 text-sm text-muted2 hover:text-terracotta">
          <ArrowLeft size={16} /> Full syllabus
        </Link>

        <div className="mt-6 flex flex-col lg:flex-row lg:items-start justify-between gap-6">
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <span className="overline">{activeItem.section_name}</span>
              <CountryBadge />
              <span className={`tag ${statusClass[activeItem.course.status]}`}>
                {statusLabel[activeItem.course.status]}
              </span>
            </div>
            <h1 className="font-heading text-4xl font-bold text-ink mt-3">{activeItem.title}</h1>
            <p className="text-lg text-muted2 mt-3 max-w-3xl">{activeItem.summary}</p>
          </div>

          <div className="flex flex-wrap gap-2 shrink-0">
            <Link to={activeItem.course.path} className="btn-primary inline-flex items-center gap-2">
              <BookOpen size={17} /> Open course
            </Link>
            <Link to={activeItem.course.practice_path} className="btn-ghost inline-flex items-center gap-2">
              <FileText size={17} /> Practice
            </Link>
          </div>
        </div>

        <div className="mt-8 grid lg:grid-cols-3 gap-5">
          <div className="lg:col-span-2 card-surface p-6">
            <div className="flex items-center gap-2">
              <Layers3 size={18} className="text-terracotta" />
              <h2 className="font-heading text-2xl font-semibold text-ink">Syllabus sub-details</h2>
            </div>
            <div className="mt-5 space-y-3">
              {activeItem.contents.map((line, index) => (
                <div key={line} className="flex items-start gap-3">
                  <span className="mt-0.5 w-6 h-6 rounded-full bg-sand text-moss text-xs font-semibold grid place-items-center">
                    {index + 1}
                  </span>
                  <p className="text-sm text-ink leading-relaxed">{line}</p>
                </div>
              ))}
            </div>
          </div>

          <aside className="space-y-5">
            <div className="card-surface p-6">
              <div className="flex items-center gap-2">
                <Map size={18} className="text-moss" />
                <h2 className="font-heading text-xl font-semibold text-ink">Course link</h2>
              </div>
              <div className="mt-4 space-y-2 text-sm">
                <div>
                  <span className="text-muted2">Topic:</span>{" "}
                  <span className="font-medium text-ink">{activeItem.course.topic_name || "Not mapped yet"}</span>
                </div>
                {activeItem.course.subtopic_name && (
                  <div>
                    <span className="text-muted2">Main lesson:</span>{" "}
                    <span className="font-medium text-ink">{activeItem.course.subtopic_name}</span>
                  </div>
                )}
                <div className={`tag mt-2 ${statusClass[activeItem.course.status]}`}>
                  {statusLabel[activeItem.course.status]}
                </div>
              </div>
            </div>

            <div className="card-surface p-6">
              <div className="flex items-center gap-2">
                <Flag size={18} className="text-terracotta" />
                <h2 className="font-heading text-xl font-semibold text-ink">Country notes</h2>
              </div>
              <div className="mt-4 space-y-3">
                {countryDetails.length === 0 ? (
                  <p className="text-sm text-muted2">No extra country-specific detail for this selection.</p>
                ) : countryDetails.map((detail) => (
                  <div key={`${detail.country}-${detail.title}`} className="rounded-lg border border-edge bg-sand/40 p-3">
                    <CountryBadge country={detail.country} />
                    <div className="font-heading font-semibold text-ink mt-2">{detail.title}</div>
                    <p className="text-sm text-muted2 mt-1">{detail.details}</p>
                  </div>
                ))}
              </div>
            </div>
          </aside>
        </div>

        {activeItem.course.related_subtopics?.length > 0 && (
          <div className="mt-8">
            <h2 className="font-heading text-2xl font-semibold text-ink">Relevant course subtopics</h2>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
              {activeItem.course.related_subtopics.map((subtopic) => (
                <div key={subtopic.id} className="card-surface p-5">
                  <div className="font-heading text-lg font-semibold text-ink">{subtopic.name}</div>
                  <div className="mt-4 flex flex-wrap gap-2">
                    {subtopic.lesson_path && (
                      <Link to={subtopic.lesson_path} className="btn-ghost !px-3 !py-2 text-sm">
                        Lesson
                      </Link>
                    )}
                    <Link to={subtopic.practice_path} className="btn-ghost !px-3 !py-2 text-sm">
                      Questions
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12 py-10" data-testid="syllabus-page">
      <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-5">
        <div>
          <span className="overline">Official syllabus map</span>
          <h1 className="font-heading text-4xl sm:text-5xl font-bold text-ink mt-2">WAEC Further Mathematics syllabus</h1>
          <p className="text-muted2 mt-3 max-w-3xl">
            Browse the full WAEC syllabus, filter country-specific areas, and jump into the linked course, lessons, or practice questions.
          </p>
          {data.source?.url && (
            <a
              href={data.source.url}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-2 text-sm text-terracotta hover:underline mt-3"
            >
              Source: {data.source.name}
            </a>
          )}
        </div>

        <div className="card-surface p-2 flex flex-wrap gap-2">
          {(data.countries || []).map((option) => (
            <button
              key={option.id}
              onClick={() => setCountry(option.id)}
              className={`px-4 py-2 rounded-lg text-sm font-heading font-semibold transition-colors ${
                country === option.id ? "bg-terracotta text-white" : "text-muted2 hover:bg-sand hover:text-ink"
              }`}
              data-testid={`country-filter-${option.id}`}
            >
              {option.name}
            </button>
          ))}
        </div>
      </div>

      <div className="grid sm:grid-cols-3 gap-4 mt-8">
        <div className="card-surface p-5">
          <div className="overline">Syllabus items</div>
          <div className="font-heading text-4xl font-bold text-ink mt-2">{data.stats.total_items}</div>
        </div>
        <div className="card-surface p-5">
          <div className="overline">Lesson-ready</div>
          <div className="font-heading text-4xl font-bold text-success mt-2">{data.stats.lesson_ready}</div>
        </div>
        <div className="card-surface p-5">
          <div className="overline">Mapped to topic</div>
          <div className="font-heading text-4xl font-bold text-moss mt-2">{data.stats.topic_ready}</div>
        </div>
      </div>

      <div className="mt-10 space-y-10">
        {data.sections.map((section) => (
          <section key={section.id} data-testid={`syllabus-section-${section.id}`}>
            <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-3">
              <div>
                <h2 className="font-heading text-3xl font-semibold text-ink">{section.name}</h2>
                <p className="text-sm text-muted2 mt-1">{section.description}</p>
              </div>
              <span className="tag">{section.paper_weight}</span>
            </div>

            <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-4 mt-5">
              {section.items.map((item) => {
                const details = visibleCountryDetails(item);
                return (
                  <Link
                    key={item.id}
                    to={`/syllabus/${item.id}${country === "all" ? "" : `?country=${country}`}`}
                    className="card-surface p-5 block group"
                    data-testid={`syllabus-item-${item.id}`}
                  >
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex items-center gap-2 flex-wrap">
                        <CountryBadge />
                        {details.map((detail) => <CountryBadge key={detail.country} country={detail.country} />)}
                      </div>
                      <ChevronRight className="text-muted2 group-hover:text-terracotta shrink-0" size={18} />
                    </div>
                    <h3 className="font-heading text-xl font-semibold text-ink group-hover:text-terracotta mt-4">
                      {item.title}
                    </h3>
                    <p className="text-sm text-muted2 mt-2 line-clamp-3">{item.summary}</p>
                    <div className="mt-4 flex items-center gap-2 flex-wrap">
                      <span className={`tag ${statusClass[item.course.status]}`}>
                        <CheckCircle2 size={13} /> {statusLabel[item.course.status]}
                      </span>
                      <span className="tag">{item.contents.length} details</span>
                    </div>
                  </Link>
                );
              })}
            </div>
          </section>
        ))}
      </div>
    </div>
  );
};

export default Syllabus;
